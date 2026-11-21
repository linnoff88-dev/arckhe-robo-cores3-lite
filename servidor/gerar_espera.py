#!/usr/bin/env python3
"""Grava a banca de frases de espera (servidor/espera.py) na voz do robô, uma vez.

  python3 servidor/gerar_espera.py            # só as que faltam
  python3 servidor/gerar_espera.py --todas    # regrava tudo (ex.: trocou a voz)
  python3 servidor/gerar_espera.py frio-01    # regrava uma
Frase com mais de 4 s é regravada (até 3 tentativas): é a voz inventando fala.

Saída: servidor/espera/<id>.wav (16 kHz, mono, 16 bits) e servidor/espera/espera.json (id, categoria, texto, voz,
duração). Usa a voz residente (servidor/voz_residente.py), que sobe se não estiver no ar.
"""
import argparse
import json
import subprocess
import sys
import wave
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
import espera  # noqa: E402
import servidor as S  # noqa: E402

PASTA = AQUI / "espera"
MAX_SEGUNDOS = 4.0  # frase de espera é curta; mais que isso é fala inventada pela voz


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--todas", action="store_true")
    ap.add_argument("ids", nargs="*", help="regravar só estes ids")
    a = ap.parse_args()
    PASTA.mkdir(exist_ok=True)
    S.garantir_voz()
    indice = []
    for ident, cat, texto in espera.ids():
        final = PASTA / f"{ident}.wav"
        refazer = a.todas or not final.exists() or ident in a.ids
        if not refazer:
            with wave.open(str(final)) as w:
                refazer = w.getnframes() / w.getframerate() > MAX_SEGUNDOS
        for tentativa in range(1, 4) if refazer else []:
            bruto = PASTA / f"{ident}.24k.wav"
            r = S._post_json(S.CFG["VOZ_URL"] + "/falar",
                             {"texto": texto, "ref": S.CFG["VOZ_REF"], "saida": str(bruto), "lang": "pt"}, 120)
            if not r.get("ok"):
                raise SystemExit(f"falhou {ident}: {r}")
            subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(bruto), "-af",
                            "silenceremove=start_periods=1:start_threshold=-45dB,areverse,"
                            "silenceremove=start_periods=1:start_threshold=-45dB,areverse",
                            "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le", str(final)], check=True)
            bruto.unlink()
            with wave.open(str(final)) as w:
                dur = w.getnframes() / w.getframerate()
            print(f"{ident} ({dur:.1f} s, tentativa {tentativa}): {texto}", flush=True)
            # O Chatterbox às vezes "inventa" fala a mais numa frase curta (frio-01 saiu com 15 s em 15/11/2026).
            if dur <= MAX_SEGUNDOS:
                break
        else:
            if refazer:
                raise SystemExit(f"{ident} passou de {MAX_SEGUNDOS} s em 3 tentativas")
        with wave.open(str(final)) as w:
            dur = w.getnframes() / w.getframerate()
        indice.append({"id": ident, "categoria": cat, "texto": texto, "segundos": round(dur, 2),
                       "voz": Path(S.CFG["VOZ_REF"]).stem})
    (PASTA / "espera.json").write_text(json.dumps(indice, ensure_ascii=False, indent=1))
    print(f"{len(indice)} frases em {PASTA}")


if __name__ == "__main__":
    main()
