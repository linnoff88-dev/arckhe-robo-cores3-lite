"""Cliente mínimo do inemavox local (só biblioteca padrão).

Só fala com 127.0.0.1. Voz só pela rota /api/jobs/tts/upload, que força o Chatterbox local:
a rota /api/jobs/tts sem "engine" cai no Edge (serviço online) e é proibida neste projeto.
"""
import json
import os
import time
import urllib.request
import uuid


class ErroInemavox(Exception):
    pass


def _multipart(campos, arquivo_campo, arquivo_caminho):
    fronteira = uuid.uuid4().hex
    partes = []
    for nome, valor in campos.items():
        partes.append(
            f"--{fronteira}\r\nContent-Disposition: form-data; name=\"{nome}\"\r\n\r\n{valor}\r\n".encode()
        )
    nome_arq = os.path.basename(arquivo_caminho)
    with open(arquivo_caminho, "rb") as f:
        dados = f.read()
    partes.append(
        f"--{fronteira}\r\nContent-Disposition: form-data; name=\"{arquivo_campo}\"; filename=\"{nome_arq}\"\r\n"
        f"Content-Type: application/octet-stream\r\n\r\n".encode() + dados + b"\r\n"
    )
    partes.append(f"--{fronteira}--\r\n".encode())
    return b"".join(partes), f"multipart/form-data; boundary={fronteira}"


class Inemavox:
    def __init__(self, url="http://127.0.0.1:8010", espera_max=180):
        if not url.startswith("http://127.0.0.1"):
            raise ValueError("inemavox só em 127.0.0.1")
        self.url = url.rstrip("/")
        self.espera_max = espera_max

    def _get(self, caminho, timeout=30):
        with urllib.request.urlopen(self.url + caminho, timeout=timeout) as r:
            return r.read()

    def _post_arquivo(self, caminho, config, arquivo):
        corpo, tipo = _multipart({"config_json": json.dumps(config, ensure_ascii=False)}, "file", arquivo)
        req = urllib.request.Request(self.url + caminho, data=corpo, headers={"Content-Type": tipo}, method="POST")
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read())

    def _esperar(self, job_id):
        inicio = time.time()
        while time.time() - inicio < self.espera_max:
            job = json.loads(self._get(f"/api/jobs/{job_id}"))
            estado = job.get("status")
            if estado == "completed":
                return job
            if estado in ("failed", "cancelled", "error"):
                raise ErroInemavox(f"job {job_id} {estado}: {str(job.get('error'))[:200]}")
            time.sleep(0.3)
        raise ErroInemavox(f"job {job_id} passou de {self.espera_max} s")

    def saude(self):
        return json.loads(self._get("/api/health", timeout=5))

    def transcrever(self, wav, modelo="large-v3", lingua="pt"):
        config = {"asr_engine": "whisper", "whisper_model": modelo, "src_lang": lingua}
        job = self._post_arquivo("/api/jobs/transcribe/upload", config, wav)
        self._esperar(job["id"])
        return self._get(f"/api/jobs/{job['id']}/transcript?format=txt").decode("utf-8").strip()

    def falar(self, texto, voz_ref, saida, lingua="pt"):
        """Gera a voz pelo Chatterbox local e grava o áudio em `saida` (formato do inemavox)."""
        job = self._post_arquivo("/api/jobs/tts/upload", {"text": texto, "lang": lingua}, voz_ref)
        self._esperar(job["id"])
        with open(saida, "wb") as f:
            f.write(self._get(f"/api/jobs/{job['id']}/audio", timeout=60))
        return saida
