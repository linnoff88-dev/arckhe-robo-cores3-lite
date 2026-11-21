#!/usr/bin/env python3
"""Voz residente do robô: Chatterbox carregado UMA vez, atende frases curtas.

O inemavox carrega o Chatterbox a cada pedido (14 a 28 s por frase, medido em 15/11/2026). Aqui o modelo fica na
memória e o processo sai sozinho depois de OCIOSO segundos parado, para liberar a GPU (mesmo padrão do
~/projetos/inemavox/whisper_daemon.py). Mesmo modelo e mesmos parâmetros do chatterbox_tts_worker.py do inemavox:
não é modelo novo. Só escuta em 127.0.0.1.

Roda no ambiente conda do inemavox:
  ~/miniconda3/envs/chatterbox/bin/python3 servidor/voz_residente.py [--porta 7872] [--ocioso 600]

  GET  /saude                                        -> {"ok": true, "device": ...}
  POST /falar {"texto": ..., "ref": wav, "saida": wav, "lang": "pt"} -> {"ok": true, "segundos": ...}
"""
import argparse
import json
import os
import re
import socket
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

ap = argparse.ArgumentParser()
ap.add_argument("--porta", type=int, default=7872)
ap.add_argument("--ocioso", type=int, default=600, help="sai depois de N s sem pedido")
ap.add_argument("--cfg-weight", type=float, default=0.65)
ap.add_argument("--exaggeration", type=float, default=0.5)
ap.add_argument("--temperature", type=float, default=0.75)
args = ap.parse_args()

# A porta antes do modelo: se já houver uma voz residente no ar, este sai sem carregar nada.
_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
_s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
try:
    _s.bind(("127.0.0.1", args.porta))
except OSError:
    raise SystemExit(f"[voz_residente] porta {args.porta} ocupada: já existe uma voz residente")
_s.close()

import soundfile as sf  # noqa: E402
import torch  # noqa: E402
from chatterbox.mtl_tts import ChatterboxMultilingualTTS  # noqa: E402

SR = 24000
t0 = time.time()
device = "cuda" if torch.cuda.is_available() else "cpu"
modelo = ChatterboxMultilingualTTS.from_pretrained(device=device)
print(f"[voz_residente] Chatterbox em {device}, carregado em {time.time()-t0:.1f}s, porta {args.porta}", flush=True)

trava = threading.Lock()
ultimo = time.time()


def falar(texto, ref, saida, lang):
    if len(re.findall(r"[A-Za-z0-9À-ɏ]", texto)) < 3:
        raise ValueError("texto curto demais")
    if not os.path.isfile(ref):
        raise ValueError(f"ref não existe: {ref}")
    lang = lang.lower().replace("-", "_").split("_")[0]
    wav = modelo.generate(texto, language_id=lang, audio_prompt_path=ref, exaggeration=args.exaggeration,
                          cfg_weight=args.cfg_weight, temperature=args.temperature)
    audio = wav.squeeze().cpu().numpy()
    sf.write(saida, audio, SR)
    return len(audio) / SR


class H(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _json(self, codigo, obj):
        corpo = json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(codigo)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(corpo)))
        self.end_headers()
        self.wfile.write(corpo)

    def do_GET(self):
        if self.path == "/saude":
            return self._json(200, {"ok": True, "device": device})
        self._json(404, {"erro": "rota"})

    def do_POST(self):
        global ultimo
        if self.path != "/falar":
            return self._json(404, {"erro": "rota"})
        try:
            req = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))))
            with trava:
                t = time.time()
                dur = falar(req["texto"], req["ref"], req["saida"], req.get("lang", "pt"))
                ultimo = time.time()
            self._json(200, {"ok": True, "segundos": round(dur, 2), "gerou_em": round(time.time() - t, 2)})
        except Exception as e:  # noqa: BLE001
            self._json(500, {"erro": str(e)[:300]})


def vigia_ocioso(srv):
    while True:
        time.sleep(10)
        if not trava.locked() and time.time() - ultimo > args.ocioso:
            print(f"[voz_residente] {args.ocioso}s parado: saindo e liberando a GPU", flush=True)
            srv.shutdown()
            return


srv = HTTPServer(("127.0.0.1", args.porta), H)
threading.Thread(target=vigia_ocioso, args=(srv,), daemon=True).start()
srv.serve_forever()
