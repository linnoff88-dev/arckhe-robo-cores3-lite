#!/usr/bin/env python3
"""Servidor do robo-cores3-lite, opção B: ouve, pensa e fala, tudo nesta máquina.

  python3 servidor/servidor.py

Um turno: WAV do robô → trava de silêncio → Whisper residente (inemavox) → claude -p pela assinatura, sem
ferramentas (com a foto, se veio) → voz residente (Chatterbox) → WAV 16 kHz mono 16 bits de volta.
Só biblioteca padrão. Só chama serviços em 127.0.0.1. Protocolo: DEFINICAO.md, seção 11.
"""
import base64
import hmac
import io
import json
import os
import re
import struct
import subprocess
import sys
import threading
import time
import urllib.parse
import urllib.request
import uuid
import wave
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
from inemavox import Inemavox  # noqa: E402
import espera  # noqa: E402

LIMITE_FALA = 1_000_000
LIMITE_FOTO = 200_000
DURACAO_MIN = 0.5
DURACAO_MAX = 15.5


def ler_env(caminho):
    cfg = {}
    if caminho.exists():
        for linha in caminho.read_text().splitlines():
            linha = linha.strip()
            if linha and not linha.startswith("#") and "=" in linha:
                k, v = linha.split("=", 1)
                cfg[k.strip()] = os.path.expanduser(v.strip())
    return cfg


CFG = {
    "ROBO_PORTA": "8770",
    "ROBO_TOKEN": "",
    "INEMAVOX_URL": "http://127.0.0.1:8010",
    "WHISPER_DAEMON_URL": "http://127.0.0.1:7871",
    "VOZ_URL": "http://127.0.0.1:7872",
    "WHISPER_MODELO": "large-v3",
    "VOZ_REF": os.path.expanduser("~/projetos/timesmkt3/media/voice-refs/rachel.wav"),
    "CLAUDE_MODELO": "haiku",
    "HISTORICO_TURNOS": "6",
    "FOTO_VALIDADE": "60",
    "SILENCIO_DB": "-50",
    "CONDA_PY": os.path.expanduser("~/miniconda3/envs/chatterbox/bin/python3"),
}
CFG.update(ler_env(AQUI / ".env"))
for chave in ("INEMAVOX_URL", "WHISPER_DAEMON_URL", "VOZ_URL"):
    if not CFG[chave].startswith("http://127.0.0.1:"):
        raise SystemExit(f"{chave} tem de ser http://127.0.0.1:<porta> (o servidor só fala com esta máquina)")
if len(CFG["ROBO_TOKEN"]) < 16 or CFG["ROBO_TOKEN"].startswith("troque"):
    raise SystemExit("ROBO_TOKEN em servidor/.env: defina um texto longo (16+ caracteres)")

DADOS = AQUI / "dados"
VAZIO = DADOS / "vazio"
for p in (DADOS / "turnos", VAZIO):
    p.mkdir(parents=True, exist_ok=True)

TURNO = threading.Lock()   # um turno por vez: a GPU é uma só
FOTOS = {}                 # turno -> (instante, caminho)
FOTOS_TRAVA = threading.Lock()
INEMAVOX = Inemavox(CFG["INEMAVOX_URL"])
ESCOLHEDOR = espera.Escolhedor()
PASTA_ESPERA = AQUI / "espera"
SUBINDO = {"whisper": threading.Lock(), "voz": threading.Lock()}  # um processo de cada, nunca dois


class Recusa(Exception):
    def __init__(self, codigo, erro, motivo=None):
        super().__init__(erro)
        self.codigo, self.erro, self.motivo = codigo, erro, motivo


def log(msg):
    print(f"{datetime.now():%H:%M:%S} {msg}", flush=True)


# ---------- serviços residentes (sobem sob demanda e saem sozinhos depois de 10 min parados) ----------

def _no_ar(url):
    try:
        urllib.request.urlopen(url + "/saude", timeout=2)
        return True
    except Exception:  # noqa: BLE001
        return False


def garantir(url, comando, nome, espera_max=120):
    if _no_ar(url):
        return 0.0
    t = time.time()
    with SUBINDO[nome]:          # quem chega depois espera o primeiro terminar de subir
        if _no_ar(url):
            return time.time() - t
        log(f"subindo {nome}")
        with open(DADOS / f"{nome}.log", "ab") as saida:
            subprocess.Popen(comando, stdout=saida, stderr=subprocess.STDOUT, start_new_session=True)
        while time.time() - t < espera_max:
            if _no_ar(url):
                return time.time() - t
            time.sleep(0.5)
    raise Recusa(503, nome)


def frio():
    return not (_no_ar(CFG["WHISPER_DAEMON_URL"]) and _no_ar(CFG["VOZ_URL"]))


def aquecer():
    """Sobe Whisper e voz em paralelo, sem esperar. O robô chama ao sentir o dedo na tela."""
    for f in (garantir_whisper, garantir_voz):
        threading.Thread(target=lambda f=f: _sem_erro(f), daemon=True).start()


def _sem_erro(f):
    try:
        f()
    except Exception as e:  # noqa: BLE001
        log(f"aquecer: {e}")


def garantir_whisper():
    porta = urllib.parse.urlparse(CFG["WHISPER_DAEMON_URL"]).port
    cmd = [CFG["CONDA_PY"], os.path.expanduser("~/projetos/inemavox/whisper_daemon.py"),
           "--porta", str(porta), "--modelo", CFG["WHISPER_MODELO"], "--ocioso", "600"]
    return garantir(CFG["WHISPER_DAEMON_URL"], cmd, "whisper")


def garantir_voz():
    porta = urllib.parse.urlparse(CFG["VOZ_URL"]).port
    cmd = [CFG["CONDA_PY"], str(AQUI / "voz_residente.py"), "--porta", str(porta), "--ocioso", "600"]
    return garantir(CFG["VOZ_URL"], cmd, "voz")


def _post_json(url, obj, timeout):
    req = urllib.request.Request(url, data=json.dumps(obj).encode(), headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())


# ---------- etapas ----------

def conferir_wav(dados):
    if dados[:4] != b"RIFF" or dados[8:12] != b"WAVE":
        raise Recusa(415, "formato")
    try:
        with wave.open(io.BytesIO(dados)) as w:
            taxa, canais, largura, quadros = w.getframerate(), w.getnchannels(), w.getsampwidth(), w.getnframes()
    except wave.Error:
        raise Recusa(415, "formato")
    if (taxa, canais, largura) != (16000, 1, 2):
        raise Recusa(415, "formato")
    return quadros / taxa


def volume_medio(caminho):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(caminho), "-af", "volumedetect", "-f", "null", "-"],
                       capture_output=True, text=True, timeout=30)
    m = re.search(r"mean_volume:\s*(-?[\d.]+|-inf)", r.stderr)
    return -999.0 if not m or m.group(1) == "-inf" else float(m.group(1))


def transcrever(wav):
    try:
        garantir_whisper()
        r = _post_json(CFG["WHISPER_DAEMON_URL"] + "/transcrever", {"audio": str(wav), "lang": "pt"}, 60)
        return " ".join(s.get("text", "").strip() for s in r.get("segments", [])).strip()
    except Recusa:
        raise
    except Exception as e:  # noqa: BLE001  — caminho lento, mas local: a fila do inemavox
        log(f"whisper residente falhou ({e}); usando a fila do inemavox")
        return INEMAVOX.transcrever(str(wav), CFG["WHISPER_MODELO"])


def historico(robo):
    arq = DADOS / f"conversa-{robo}.json"
    try:
        return json.loads(arq.read_text())
    except Exception:  # noqa: BLE001
        return []


def guardar_historico(robo, ouvido, resposta):
    arq = DADOS / f"conversa-{robo}.json"
    trocas = historico(robo) + [{"pessoa": ouvido, "robo": resposta, "quando": datetime.now().isoformat(timespec="seconds")}]
    arq.write_text(json.dumps(trocas[-50:], ensure_ascii=False, indent=1))


class ClaudePronto:
    """Um `claude -p` já aberto esperando a próxima pergunta: a partida do processo sai da espera (~1,2 s).

    Sempre pela assinatura (sem ANTHROPIC_API_KEY), sem ferramentas, sem MCP, sem sessão salva, numa pasta vazia.
    """
    def __init__(self):
        self.trava = threading.Lock()
        self.proc = None

    def _abrir(self):
        env = {k: v for k, v in os.environ.items() if k != "ANTHROPIC_API_KEY"}
        cmd = ["claude", "-p", "--model", CFG["CLAUDE_MODELO"], "--tools", "", "--strict-mcp-config",
               "--no-session-persistence", "--input-format", "stream-json", "--output-format", "stream-json",
               "--verbose", "--system-prompt", (AQUI / "persona.txt").read_text()]
        return subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                text=True, cwd=VAZIO, env=env, start_new_session=True)

    def pegar(self):
        with self.trava:
            proc, self.proc = self.proc, None
        if proc is None or proc.poll() is not None:
            proc = self._abrir()
        return proc

    def repor(self):
        def abrir():
            novo = self._abrir()
            with self.trava:
                velho, self.proc = self.proc, novo
            if velho is not None and velho.poll() is None:
                velho.kill()
        threading.Thread(target=abrir, daemon=True).start()


CLAUDE = ClaudePronto()

# Trava de cota compartilhada (17/11/2026): mesma tabela `pools` do EngineBridge e do ia_motor.py
# (~/.local/state/enginebridge/state.sqlite). Falha do banco = segue sem trava.
COTA_DB = Path(os.environ.get("INEMA_COTA_DB", Path.home() / ".local/state/enginebridge/state.sqlite")).expanduser()
COTA_POOL = "claude:" + str(Path(os.environ.get("CLAUDE_CONFIG_DIR", Path.home() / ".claude")).expanduser())


def cota_travada():
    import sqlite3
    try:
        with sqlite3.connect(COTA_DB, timeout=5) as db:
            linha = db.execute("SELECT blocked, until FROM pools WHERE pool=?", (COTA_POOL,)).fetchone()
    except sqlite3.Error:
        return None
    if linha and (linha[0] or linha[1] > time.time()):
        return "claude sem cota (trava compartilhada)"
    return None


def cota_registrar(ate):
    import sqlite3
    try:
        COTA_DB.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        with sqlite3.connect(COTA_DB, timeout=5) as db:
            db.execute("CREATE TABLE IF NOT EXISTS pools (pool TEXT PRIMARY KEY, blocked INTEGER DEFAULT 0, until REAL DEFAULT 0, owner TEXT, lease REAL DEFAULT 0)")
            db.execute("INSERT INTO pools(pool, until) VALUES (?, ?) ON CONFLICT(pool) DO UPDATE SET until=MAX(pools.until, excluded.until)",
                       (COTA_POOL, ate))
    except sqlite3.Error:
        pass


def pensar(robo, ouvido, foto):
    n = int(CFG["HISTORICO_TURNOS"])
    linhas = [f"Agora: {datetime.now():%d/%m/%Y %H:%M} (horário de Brasília)."]
    antes = historico(robo)[-n:]
    if antes:
        linhas.append("Conversa até aqui:")
        linhas += [f"Pessoa: {t['pessoa']}\nVocê: {t['robo']}" for t in antes]
    linhas.append(f"A pessoa disse agora: {ouvido}")
    conteudo = []
    if foto:
        conteudo.append({"type": "image", "source": {"type": "base64", "media_type": "image/jpeg",
                                                      "data": base64.b64encode(foto.read_bytes()).decode()}})
        linhas.append("(A imagem acima é o que a sua câmera está vendo agora.)")
    conteudo.append({"type": "text", "text": "\n".join(linhas)})
    entrada = json.dumps({"type": "user", "message": {"role": "user", "content": conteudo}}, ensure_ascii=False)

    cota = cota_travada()
    if cota:                       # trava de cota compartilhada: sem cota, responde na hora
        log(cota)
        raise Recusa(503, "claude sem cota")
    proc = CLAUDE.pegar()
    try:
        saida, erro = proc.communicate(entrada + "\n", timeout=90)
    finally:
        CLAUDE.repor()
    r = subprocess.CompletedProcess(proc.args, proc.returncode, saida, erro)
    for linha in r.stdout.splitlines():
        try:
            d = json.loads(linha)
        except json.JSONDecodeError:
            continue
        if d.get("type") == "result":
            if d.get("is_error") and d.get("api_error") == "usage_limit_reached":
                cota_registrar(time.time() + 3600)   # sem ler o horário: 1 h; o ia_motor.py grava o exato
                raise Recusa(503, "claude sem cota")
            if d.get("is_error") or not (d.get("result") or "").strip():
                raise Recusa(500, "claude")
            return limpar_fala(d["result"])
    log(f"claude sem resultado: rc={r.returncode} {r.stderr[:200]}")
    raise Recusa(500, "claude")


def limpar_fala(texto):
    texto = re.sub(r"[*_#`>|~]", "", texto)
    texto = re.sub(r"\s+", " ", texto).strip()
    return texto[:600]


NUMEROS = set("""zero um uma dois duas tres três quatro cinco seis sete oito nove dez onze doze treze catorze quatorze
quinze dezesseis dezessete dezoito dezenove vinte trinta quarenta cinquenta sessenta setenta oitenta noventa cem cento
duzentos trezentos quatrocentos quinhentos seiscentos setecentos oitocentos novecentos mil milhao milhão milhoes milhões
meia meio""".split())
NAO_CORTAR = NUMEROS | {"e", "de", "da", "do", "das", "dos", "a", "o", "as", "os", "um", "uma", "em", "no", "na"}


def _corte_seguro(frase, depois_de):
    """Primeiro espaço depois de `depois_de` que não fica no meio de um número nem antes de artigo/preposição."""
    palavras = frase.split(" ")
    pos = 0
    for i, p in enumerate(palavras[:-1]):
        pos += len(p) + 1
        if pos < depois_de or len(frase) - pos < 15:
            continue
        atual = p.lower().strip(",.;:")
        seguinte = palavras[i + 1].lower().strip(",.;:")
        if atual not in NAO_CORTAR and seguinte not in NUMEROS and seguinte != "e":
            return pos
    return None


def partes(texto, minimo=30):
    """Divide a resposta em frases para a voz começar pela primeira. Frase curta junta com a seguinte."""
    pedacos = [p.strip() for p in re.split(r"(?<=[.!?…])\s+", texto) if p.strip()]
    # A primeira parte decide quando sai o primeiro som: se for longa, corta na primeira vírgula.
    # Ordem: vírgula/dois-pontos/ponto e vírgula entre o 10º e o 60º caractere; senão, o espaço depois do 35º.
    if pedacos and len(pedacos[0]) > 50:
        m = re.search(r"[,:;]\s", pedacos[0][10:60])
        corte = 10 + m.end() if m else None
        if corte is None:
            corte = _corte_seguro(pedacos[0], 35)
        if corte:
            pedacos[0:1] = [pedacos[0][:corte].strip(), pedacos[0][corte:].strip()]
    saida = []
    for p in pedacos:
        if len(saida) > 1 and len(saida[-1]) < minimo:
            saida[-1] += " " + p
        else:
            saida.append(p)
    return saida or [texto]


def falar(texto, pasta, nome="resposta"):
    garantir_voz()
    bruto = pasta / f"{nome}-24k.wav"
    r = _post_json(CFG["VOZ_URL"] + "/falar", {"texto": texto, "ref": CFG["VOZ_REF"], "saida": str(bruto), "lang": "pt"}, 120)
    if not r.get("ok"):
        raise Recusa(500, "voz")
    final = pasta / f"{nome}.wav"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(bruto), "-ar", "16000", "-ac", "1",
                    "-c:a", "pcm_s16le", str(final)], check=True, timeout=60)
    return final


def preparar(dados, turno_foto):
    """Confere o WAV e acha a foto. Tudo que pode recusar o pedido acontece aqui, antes de responder."""
    pasta = DADOS / "turnos" / f"{datetime.now():%Y%m%d-%H%M%S}-{uuid.uuid4().hex[:4]}"
    pasta.mkdir(parents=True)
    pergunta = pasta / "pergunta.wav"
    pergunta.write_bytes(dados)

    duracao = conferir_wav(dados)
    if duracao < DURACAO_MIN:
        raise Recusa(204, "curta", "curta")
    if duracao > DURACAO_MAX:
        raise Recusa(413, "grande")
    vol = volume_medio(pergunta)
    if vol < float(CFG["SILENCIO_DB"]):
        raise Recusa(204, "silencio", f"silencio ({vol:.1f} dB)")

    foto = None
    if turno_foto:
        with FOTOS_TRAVA:
            achado = FOTOS.pop(turno_foto, None)
        if achado and time.time() - achado[0] <= float(CFG["FOTO_VALIDADE"]):
            foto = pasta / "foto.jpg"
            foto.write_bytes(Path(achado[1]).read_bytes())
    return pasta, pergunta, foto


def turno(robo, dados, turno_foto):
    """/v1/fala: um WAV inteiro de volta (simples; usado nos testes e como reserva)."""
    tempos = {}
    t0 = time.time()
    pasta, pergunta, foto = preparar(dados, turno_foto)

    with TURNO:
        t = time.time()
        ouvido = transcrever(pergunta)
        tempos["stt"] = time.time() - t
        if not re.search(r"\w", ouvido):
            raise Recusa(204, "vazio", "sem texto")
        t = time.time()
        resposta = pensar(robo, ouvido, foto)
        tempos["llm"] = time.time() - t
        t = time.time()
        wav = falar(resposta, pasta)
        tempos["tts"] = time.time() - t
    tempos["total"] = time.time() - t0
    guardar_historico(robo, ouvido, resposta)
    (pasta / "turno.json").write_text(json.dumps({"robo": robo, "ouvido": ouvido, "resposta": resposta,
                                                  "foto": bool(foto), "tempos": tempos}, ensure_ascii=False, indent=1))
    log(f"OUVIDO: {ouvido} | RESPOSTA: {resposta} | " + " ".join(f"{k}={v:.1f}" for k, v in tempos.items()))
    return ouvido, resposta, tempos, wav.read_bytes()


def registrar(pasta, robo, ouvido, resposta, foto, tempos, extra=None):
    guardar_historico(robo, ouvido, resposta)
    info = {"robo": robo, "ouvido": ouvido, "resposta": resposta, "foto": bool(foto), "tempos": tempos}
    info.update(extra or {})
    (pasta / "turno.json").write_text(json.dumps(info, ensure_ascii=False, indent=1))
    log(f"OUVIDO: {ouvido} | RESPOSTA: {resposta} | " + " ".join(f"{k}={v:.1f}" for k, v in tempos.items()))


def quadro(tipo, dados):
    """Um quadro do fluxo /v1/conversa: 1 byte de tipo + 4 bytes de tamanho (little-endian) + dados."""
    if isinstance(dados, str):
        dados = dados.encode("utf-8")
    elif isinstance(dados, (dict, list)):
        dados = json.dumps(dados, ensure_ascii=False).encode("utf-8")
    return tipo.encode() + struct.pack("<I", len(dados)) + dados


def conversa(robo, pasta, pergunta, foto, enviar, t0):
    """/v1/conversa: manda os quadros assim que cada etapa termina.

    O = o que ouviu · E = frase de espera (id da banca) · T = texto de uma parte · A = WAV dessa parte · F = fim.
    """
    tempos = {}
    espera_usada = None
    with TURNO:
        if frio():
            aquecer()
            escolha = ESCOLHEDOR.escolher(robo, "frio", frio=True)
            if escolha:
                espera_usada = escolha
                enviar(quadro("E", escolha[0]))
        t = time.time()
        ouvido = transcrever(pergunta)
        tempos["stt"] = time.time() - t
        if not re.search(r"\w", ouvido):
            enviar(quadro("F", {"vazio": True}))
            return
        enviar(quadro("O", ouvido))
        tempos["ouvido_em"] = time.time() - t0
        if espera_usada is None:
            escolha = ESCOLHEDOR.escolher(robo, espera.categoria(ouvido, bool(foto)))
            if escolha:
                espera_usada = escolha
                enviar(quadro("E", escolha[0]))
        t = time.time()
        resposta = pensar(robo, ouvido, foto)
        tempos["llm"] = time.time() - t
        t = time.time()
        for n, parte in enumerate(partes(resposta), 1):
            wav = falar(parte, pasta, f"resposta-{n}")
            enviar(quadro("T", parte))
            enviar(quadro("A", wav.read_bytes()))
            if n == 1:
                tempos["primeiro_som"] = time.time() - t0
        tempos["tts"] = time.time() - t
    tempos["total"] = time.time() - t0
    enviar(quadro("F", {"resposta": resposta, "tempos": {k: round(v, 2) for k, v in tempos.items()},
                        "espera": espera_usada[0] if espera_usada else None}))
    registrar(pasta, robo, ouvido, resposta, foto, tempos,
              {"espera": espera_usada[1] if espera_usada else None, "partes": len(partes(resposta))})


# ---------- HTTP ----------

class Robo(BaseHTTPRequestHandler):
    server_version = "robo-cores3-lite"
    protocol_version = "HTTP/1.1"

    def log_message(self, *a):
        pass

    def _responder(self, codigo, corpo=b"", tipo="application/json", extras=None):
        self.send_response(codigo)
        if codigo != 204:
            self.send_header("Content-Type", tipo)
            self.send_header("Content-Length", str(len(corpo)))
        for k, v in (extras or {}).items():
            self.send_header(k, v)
        self.end_headers()
        if codigo != 204 and corpo:
            self.wfile.write(corpo)

    def _erro(self, codigo, erro, motivo=None):
        extras = {"X-Motivo": urllib.parse.quote(motivo)} if motivo else None
        if codigo == 204:
            self._responder(204, extras=extras)
        else:
            self._responder(codigo, json.dumps({"erro": erro}).encode(), extras=extras)

    def _corpo(self, limite):
        tamanho = int(self.headers.get("Content-Length") or 0)
        if tamanho > limite:
            # lê e descarta para não deixar o cliente pendurado
            restante = tamanho
            while restante > 0:
                bloco = self.rfile.read(min(65536, restante))
                if not bloco:
                    break
                restante -= len(bloco)
            raise Recusa(413, "grande")
        return self.rfile.read(tamanho)

    def _token_ok(self):
        return hmac.compare_digest(self.headers.get("X-Robo-Token", ""), CFG["ROBO_TOKEN"])

    def do_GET(self):
        if self.path == "/saude":
            return self._responder(200, b'{"ok": true}')
        if self.path.startswith("/v1/espera"):
            if not self._token_ok():
                return self._erro(401, "token")
            if self.path == "/v1/espera":   # a placa baixa a banca uma vez e guarda na memória dela
                return self._responder(200, (PASTA_ESPERA / "espera.json").read_bytes())
            m = re.fullmatch(r"/v1/espera/([a-z]+-\d{2})\.wav", self.path)
            if m and (PASTA_ESPERA / f"{m.group(1)}.wav").exists():
                return self._responder(200, (PASTA_ESPERA / f"{m.group(1)}.wav").read_bytes(), "audio/wav")
        self._erro(404, "rota")

    def do_POST(self):
        robo = re.sub(r"[^A-Za-z0-9_-]", "", self.headers.get("X-Robo-Id", "robo"))[:32] or "robo"
        try:
            if self.path not in ("/v1/fala", "/v1/foto", "/v1/conversa", "/v1/aquecer"):
                raise Recusa(404, "rota")
            if not self._token_ok():
                self._corpo(LIMITE_FALA * 3)
                raise Recusa(401, "token")
            if self.path == "/v1/aquecer":
                self._corpo(1024)
                estava_frio = frio()
                if estava_frio:
                    aquecer()
                return self._responder(202, json.dumps({"frio": estava_frio}).encode())
            if self.path == "/v1/conversa":
                dados = self._corpo(LIMITE_FALA)
                t0 = time.time()
                pasta, pergunta, foto = preparar(dados, self.headers.get("X-Turno"))
                self.send_response(200)
                self.send_header("Content-Type", "application/x-robo-quadros")
                self.send_header("Connection", "close")
                self.end_headers()
                self.close_connection = True

                def enviar(b):
                    self.wfile.write(b)
                    self.wfile.flush()
                try:
                    conversa(robo, pasta, pergunta, foto, enviar, t0)
                except Exception as e:  # noqa: BLE001  — o 200 já saiu: o erro vai num quadro X
                    erro = e.erro if isinstance(e, Recusa) else "servidor"
                    log(f"/v1/conversa erro no meio: {type(e).__name__}: {e}")
                    try:
                        enviar(quadro("X", {"erro": erro}))
                    except OSError:
                        pass
                return
            if self.path == "/v1/foto":
                dados = self._corpo(LIMITE_FOTO)
                if dados[:3] != b"\xff\xd8\xff":
                    raise Recusa(415, "formato")
                tid = uuid.uuid4().hex[:12]
                caminho = DADOS / f"foto-{tid}.jpg"
                caminho.write_bytes(dados)
                with FOTOS_TRAVA:
                    agora = time.time()
                    for k in [k for k, (t, _) in FOTOS.items() if agora - t > float(CFG["FOTO_VALIDADE"])]:
                        Path(FOTOS.pop(k)[1]).unlink(missing_ok=True)
                    FOTOS[tid] = (agora, str(caminho))
                return self._responder(200, json.dumps({"turno": tid}).encode())
            dados = self._corpo(LIMITE_FALA)
            ouvido, resposta, tempos, wav = turno(robo, dados, self.headers.get("X-Turno"))
            q = lambda s: urllib.parse.quote(s[:500])  # noqa: E731
            self._responder(200, wav, "audio/wav", {
                "X-Ouvido": q(ouvido), "X-Resposta": q(resposta),
                "X-Tempos": ";".join(f"{k}={v:.1f}" for k, v in tempos.items())})
        except Recusa as r:
            if r.codigo != 204:
                log(f"{self.path} {r.codigo} {r.erro}")
            self._erro(r.codigo, r.erro, r.motivo)
        except Exception as e:  # noqa: BLE001
            log(f"{self.path} 500 {type(e).__name__}: {e}")
            self._erro(500, "servidor")


def main():
    porta = int(CFG["ROBO_PORTA"])
    srv = ThreadingHTTPServer(("0.0.0.0", porta), Robo)
    CLAUDE.repor()   # o primeiro claude -p já fica aberto esperando
    log(f"robo-cores3-lite ouvindo na porta {porta} (voz: {Path(CFG['VOZ_REF']).stem}, modelo: {CFG['CLAUDE_MODELO']})")
    srv.serve_forever()


if __name__ == "__main__":
    main()
