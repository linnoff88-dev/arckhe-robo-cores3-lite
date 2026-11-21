#!/usr/bin/env python3
"""Validador da F1 (PLANO.md). Precisa do servidor no ar: python3 servidor/servidor.py

  python3 servidor/testar.py servidor/teste/pergunta.wav
  python3 servidor/testar.py --foto servidor/teste/foto.jpg servidor/teste/pergunta-visao.wav
  python3 servidor/testar.py --limites
  python3 servidor/testar.py --conversa servidor/teste/pergunta.wav          # resposta por partes
  python3 servidor/testar.py --conversa --frio servidor/teste/pergunta.wav   # desliga os residentes antes e
                                                                             # chama /v1/aquecer como o robô faz

Termina com PASSOU (código 0) ou FALHOU (código 1). Cada turno que passa entra em servidor/MEDIDAS.md.
"""
import argparse
import http.client
import time
import io
import json
import math
import os
import re
import struct
import subprocess
import sys
import tempfile
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
import wave
from datetime import datetime
from pathlib import Path

AQUI = Path(__file__).resolve().parent
ROBO_ID = "teste-" + os.urandom(3).hex()   # conversa nova a cada execução: o histórico de um teste não vaza no outro
sys.path.insert(0, str(AQUI))
from servidor import ler_env  # noqa: E402  (só lê o .env; não sobe nada)

CFG = {"ROBO_PORTA": "8770", "ROBO_TOKEN": "", "WHISPER_DAEMON_URL": "http://127.0.0.1:7871"}
CFG.update(ler_env(AQUI / ".env"))
BASE = f"http://127.0.0.1:{CFG['ROBO_PORTA']}"
falhas = []


def checar(ok, msg):
    print(("  ok    " if ok else "  FALHA ") + msg)
    if not ok:
        falhas.append(msg)


def post(rota, corpo, tipo, token=None, extras=None, timeout=150):
    h = {"Content-Type": tipo, "X-Robo-Token": CFG["ROBO_TOKEN"] if token is None else token, "X-Robo-Id": ROBO_ID}
    h.update(extras or {})
    req = urllib.request.Request(BASE + rota, data=corpo, headers=h, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, dict(r.headers), r.read()
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers), e.read()


def volume(caminho):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(caminho), "-af", "volumedetect", "-f", "null", "-"],
                       capture_output=True, text=True)
    m = re.search(r"mean_volume:\s*(-?[\d.]+)", r.stderr)
    return float(m.group(1)) if m else -999.0


NUMEROS = set("""zero um uma dois duas tres quatro cinco seis sete oito nove dez onze doze treze catorze quatorze
quinze dezesseis dezessete dezoito dezenove vinte trinta quarenta cinquenta sessenta setenta oitenta noventa cem
cento duzentos trezentos quatrocentos quinhentos seiscentos setecentos oitocentos novecentos mil meia meio e h""".split())


def palavras(texto):
    """Palavras para comparar a voz com o texto. Números ficam de fora: a resposta vem por extenso
    ("treze e vinte") e o Whisper escreve em algarismos ("13h20") — a diferença é de grafia, não de voz."""
    t = unicodedata.normalize("NFKD", texto.lower())
    t = "".join(c for c in t if not unicodedata.combining(c))
    return [p for p in re.findall(r"[a-z0-9]+", t) if p not in NUMEROS and not any(ch.isdigit() for ch in p)]


def transcrever(caminho):
    req = urllib.request.Request(CFG["WHISPER_DAEMON_URL"] + "/transcrever",
                                 data=json.dumps({"audio": str(caminho), "lang": "pt"}).encode(),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return " ".join(s.get("text", "") for s in json.loads(r.read()).get("segments", []))


def wav_bytes(segundos, amplitude=0.0, freq=440):
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(16000)
        n = int(segundos * 16000)
        w.writeframes(b"".join(struct.pack("<h", int(amplitude * 32767 * math.sin(2 * math.pi * freq * i / 16000)))
                               for i in range(n)))
    return buf.getvalue()


def um_turno(wav, foto):
    extras = {}
    if foto:
        st, _, corpo = post("/v1/foto", Path(foto).read_bytes(), "image/jpeg")
        checar(st == 200, f"/v1/foto → {st}")
        if st == 200:
            extras["X-Turno"] = json.loads(corpo)["turno"]
    st, h, corpo = post("/v1/fala", Path(wav).read_bytes(), "audio/wav", extras=extras)
    checar(st == 200, f"/v1/fala → {st}")
    if st != 200:
        return
    ouvido = urllib.parse.unquote(h.get("X-Ouvido", ""))
    resposta = urllib.parse.unquote(h.get("X-Resposta", ""))
    tempos = h.get("X-Tempos", "")
    print(f"OUVIDO: {ouvido}\nRESPOSTA: {resposta}\nTEMPOS: {tempos}")
    saida = AQUI / "teste" / "resposta.wav"
    saida.write_bytes(corpo)

    fmt = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_name,sample_rate,channels",
                          "-of", "csv=p=0", str(saida)], capture_output=True, text=True).stdout.strip()
    checar(fmt == "pcm_s16le,16000,1", f"formato da resposta: {fmt}")
    vol = volume(saida)
    checar(vol > -40, f"volume médio da resposta: {vol:.1f} dB (precisa > -40)")
    ouvido_resp = transcrever(saida)
    esperadas, achadas = palavras(resposta), set(palavras(ouvido_resp))
    taxa = sum(p in achadas for p in esperadas) / max(1, len(esperadas))
    checar(taxa >= 0.8, f"voz bate com o texto: {taxa:.0%} das palavras (precisa 80%)")
    if foto:
        print(f"  (conferir a olho: a resposta fala do que está em {foto}?)")
    if not falhas:
        medidas = AQUI / "MEDIDAS.md"
        if not medidas.exists():
            medidas.write_text("# MEDIDAS — tempos do servidor (opção B)\n\n"
                               "Segundos. stt = Whisper residente, llm = claude -p, tts = voz residente.\n\n"
                               "| quando | teste | foto | stt | llm | tts | total | ouvido |\n|---|---|---|---|---|---|---|---|\n")
        t = dict(kv.split("=") for kv in tempos.split(";") if "=" in kv)
        with medidas.open("a") as f:
            f.write(f"| {datetime.now():%d/%m/%Y %H:%M:%S} | {Path(wav).name} | {'sim' if foto else 'não'} | "
                    f"{t.get('stt')} | {t.get('llm')} | {t.get('tts')} | {t.get('total')} | {ouvido} |\n")


def ler_quadros(resp):
    while True:
        cab = resp.read(5)
        if len(cab) < 5:
            return
        tipo, n = chr(cab[0]), struct.unpack("<I", cab[1:])[0]
        dados = b""
        while len(dados) < n:
            bloco = resp.read(n - len(dados))
            if not bloco:
                break
            dados += bloco
        yield tipo, dados


def desligar_residentes():
    r = subprocess.run(["pgrep", "-f", "voz_residente.py|whisper_daemon.py"], capture_output=True, text=True)
    for pid in r.stdout.split():
        subprocess.run(["kill", pid])
    time.sleep(3)


def uma_conversa(wav, foto, frio):
    if frio:
        desligar_residentes()
        t_toque = time.time()
        st, _, corpo = post("/v1/aquecer", b"", "application/octet-stream")
        checar(st == 202, f"/v1/aquecer → {st} {corpo.decode()}")
        dur = wave.open(str(wav)).getnframes() / 16000
        time.sleep(dur)          # o robô aquece quando o dedo encosta; a pessoa fala; depois manda
    extras = {}
    if foto:
        st, _, corpo = post("/v1/foto", Path(foto).read_bytes(), "image/jpeg")
        extras["X-Turno"] = json.loads(corpo)["turno"]
    con = http.client.HTTPConnection("127.0.0.1", int(CFG["ROBO_PORTA"]), timeout=180)
    h = {"Content-Type": "audio/wav", "X-Robo-Token": CFG["ROBO_TOKEN"], "X-Robo-Id": ROBO_ID}
    h.update(extras)
    t0 = time.time()
    con.request("POST", "/v1/conversa", body=Path(wav).read_bytes(), headers=h)
    resp = con.getresponse()
    checar(resp.status == 200, f"/v1/conversa → {resp.status}")
    if resp.status != 200:
        return
    chegou, partes_wav, textos, fim, esp = {}, [], [], {}, None
    for tipo, dados in ler_quadros(resp):
        agora = time.time() - t0
        chegou.setdefault(tipo, agora)
        if tipo == "O":
            print(f"OUVIDO ({agora:.1f} s): {dados.decode()}")
        elif tipo == "E":
            esp = dados.decode()
            texto = next((x["texto"] for x in json.loads((AQUI / "espera" / "espera.json").read_text()) if x["id"] == esp), "?")
            print(f"ESPERA ({agora:.1f} s): {esp} — {texto}")
        elif tipo == "T":
            textos.append(dados.decode())
            print(f"PARTE ({agora:.1f} s): {dados.decode()}")
        elif tipo == "A":
            partes_wav.append(dados)
        elif tipo == "F":
            fim = json.loads(dados)
        elif tipo == "X":
            checar(False, f"erro no meio: {dados.decode()}")
    checar(bool(partes_wav) and len(partes_wav) == len(textos), f"{len(partes_wav)} partes de áudio, {len(textos)} de texto")
    if not partes_wav:
        return
    lista = AQUI / "teste" / "conversa-lista.txt"
    arquivos = []
    for i, b in enumerate(partes_wav, 1):
        f = AQUI / "teste" / f"conversa-{i}.wav"
        f.write_bytes(b)
        arquivos.append(f)
    lista.write_text("".join(f"file '{f}'\n" for f in arquivos))
    saida = AQUI / "teste" / "resposta-conversa.wav"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lista), "-c", "copy", str(saida)], check=True)
    for f in arquivos + [lista]:
        f.unlink()
    fmt = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_name,sample_rate,channels",
                          "-of", "csv=p=0", str(saida)], capture_output=True, text=True).stdout.strip()
    checar(fmt == "pcm_s16le,16000,1", f"formato: {fmt}")
    vol = volume(saida)
    checar(vol > -40, f"volume médio: {vol:.1f} dB")
    resposta = " ".join(textos)
    esperadas, achadas = palavras(resposta), set(palavras(transcrever(saida)))
    taxa = sum(p in achadas for p in esperadas) / max(1, len(esperadas))
    checar(taxa >= 0.8, f"voz bate com o texto: {taxa:.0%}")
    primeiro = chegou.get("A", 0)
    meta = 20 if frio else 8
    base = f"{primeiro:.1f} s depois de enviar" + (f" ({primeiro + dur:.1f} s depois do toque)" if frio else "")
    checar(primeiro < meta, f"primeiro som: {base} (meta < {meta} s)")
    print(f"TEMPOS: {fim.get('tempos')}")
    if not falhas:
        medidas = AQUI / "MEDIDAS.md"
        t = fim.get("tempos", {})
        with medidas.open("a") as f:
            f.write(f"| {datetime.now():%d/%m/%Y %H:%M:%S} | conversa{' fria' if frio else ''} {Path(wav).name} | "
                    f"{'sim' if foto else 'não'} | {t.get('stt')} | {t.get('llm')} | {t.get('tts')} | "
                    f"{t.get('total')} (1º som {t.get('primeiro_som')}) | {esp or '-'} |\n")


def limites():
    wav_ok = (AQUI / "teste" / "pergunta.wav").read_bytes()
    st, _, _ = post("/v1/fala", wav_ok, "audio/wav", token="errado-errado-errado")
    checar(st == 401, f"token errado → {st} (esperado 401)")
    st, _, _ = post("/v1/fala", b"\0" * 2_000_000, "audio/wav")
    checar(st == 413, f"fala de 2 MB → {st} (esperado 413)")
    st, _, _ = post("/v1/foto", b"\xff\xd8\xff" + b"\0" * 300_000, "image/jpeg")
    checar(st == 413, f"foto de 300 kB → {st} (esperado 413)")
    st, h, _ = post("/v1/fala", wav_bytes(3.0), "audio/wav")
    motivo = urllib.parse.unquote(h.get("X-Motivo", ""))
    checar(st == 204 and motivo.startswith("silencio"), f"3 s de silêncio → {st} {motivo} (esperado 204 silencio, sem Whisper)")
    st, _, _ = post("/v1/fala", b"isto nao e um wav" * 100, "audio/wav")
    checar(st == 415, f"arquivo que não é WAV → {st} (esperado 415)")
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(44100); w.writeframes(b"\0" * 44100 * 4)
    st, _, _ = post("/v1/fala", buf.getvalue(), "audio/wav")
    checar(st == 415, f"WAV 44,1 kHz estéreo → {st} (esperado 415)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("wav", nargs="?")
    ap.add_argument("--foto")
    ap.add_argument("--limites", action="store_true")
    ap.add_argument("--conversa", action="store_true")
    ap.add_argument("--frio", action="store_true")
    a = ap.parse_args()
    try:
        urllib.request.urlopen(BASE + "/saude", timeout=3)
    except Exception:  # noqa: BLE001
        print(f"FALHOU: servidor fora do ar em {BASE}")
        sys.exit(1)
    if a.limites:
        limites()
    elif a.wav and a.conversa:
        uma_conversa(a.wav, a.foto, a.frio)
    elif a.wav:
        um_turno(a.wav, a.foto)
    else:
        ap.error("passe um WAV ou --limites")
    print("PASSOU" if not falhas else f"FALHOU ({len(falhas)})")
    sys.exit(0 if not falhas else 1)


if __name__ == "__main__":
    main()
