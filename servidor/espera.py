"""Frases de espera do robô: o que ele diz enquanto pensa, sem ficar repetitivo.

A banca é gravada uma vez na voz do robô (servidor/gerar_espera.py → servidor/espera/<id>.wav) e copiada para a
placa, que toca na hora, sem gastar GPU. O servidor só escolhe QUAL tocar (ou nenhuma) e manda o id.

Regras (pedido do Nei, 15/11/2026: "criar interações para amortecer a espera, sem ser repetitivo"):
- a categoria vem do que a pessoa disse (hora, foto, conta, pergunta difícil...);
- nunca repete uma das últimas 8 que tocaram para aquele robô;
- pula de vez em quando (1 vez em 3) para não virar tique; nunca pula no caso frio (a espera é longa);
- saudação curta não ganha frase de espera: a resposta é rápida.
"""
import random
import re
import threading
import unicodedata
from collections import defaultdict, deque

BANCA = {
    "frio": [
        "Opa, eu estava cochilando. Só um instante.",
        "Hum, acordando aqui. Já te respondo.",
        "Espera, deixa eu esfregar os olhos.",
        "Ligando os motores da cabeça, um momento.",
    ],
    "hora": [
        "Deixa eu olhar o relógio.",
        "Um segundo, vou ver as horas.",
        "Deixa eu fazer a conta do fuso.",
        "Hum, que horas são mesmo? Já vejo.",
    ],
    "foto": [
        "Deixa eu olhar direito.",
        "Hum, deixa eu ver o que tem aqui.",
        "Peraí, focando a câmera.",
        "Olhando com atenção.",
        "Deixa eu enxergar melhor.",
    ],
    "conta": [
        "Calculando aqui.",
        "Deixa eu fazer essa conta.",
        "Hum, números. Só um instante.",
        "Somando tudo aqui.",
    ],
    "dificil": [
        "Boa pergunta, deixa eu pensar.",
        "Hum, essa é interessante.",
        "Deixa eu organizar as ideias.",
        "Pergunta boa. Pensando aqui.",
        "Essa merece uma boa resposta. Um instante.",
    ],
    "geral": [
        "Hum, deixa eu ver.",
        "Só um instante.",
        "Pensando aqui.",
        "Um momento.",
        "Deixa comigo.",
        "Já te digo.",
        "Hum.",
        "Entendi. Um segundo.",
        "Certo, deixa eu pensar.",
        "Tá bom, já respondo.",
    ],
}

_RE = {
    "hora": r"\b(hora|horas|horario|que dia|data|hoje|amanha|ontem|fuso|relogio|minutos?)\b",
    "conta": r"(\d+\s*(mais|menos|vezes|x|dividido)\s*\d+|\bquanto (e|da|fica|custa)\b|\bcalcul|\bsoma|\bporcentagem|\braiz)",
    "dificil": r"\b(por que|porque|como funciona|explica|explique|qual a diferenca|o que acontece|significa|sentido)\b",
    "saudacao": r"^(oi|ola|e ai|bom dia|boa tarde|boa noite|tudo bem|obrigad[oa]|valeu|tchau)\b",
}


def _normal(texto):
    t = unicodedata.normalize("NFKD", texto.lower())
    return "".join(c for c in t if not unicodedata.combining(c)).strip()


def ids():
    """Lista estável (id, categoria, texto) de toda a banca. O id é <categoria>-<nn>."""
    return [(f"{cat}-{i:02d}", cat, frase) for cat, frases in BANCA.items() for i, frase in enumerate(frases, 1)]


def categoria(ouvido, com_foto):
    t = _normal(ouvido)
    if com_foto:
        return "foto"
    for cat in ("hora", "conta", "dificil"):
        if re.search(_RE[cat], t):
            return cat
    if re.search(_RE["saudacao"], t) and len(t.split()) <= 5:
        return None
    return "geral"


class Escolhedor:
    def __init__(self, memoria=8, pular=1 / 3, sorteio=None):
        self.recentes = defaultdict(lambda: deque(maxlen=memoria))
        self.pular = pular
        self.rnd = sorteio or random.Random()
        self.trava = threading.Lock()

    def escolher(self, robo, cat, frio=False):
        """Devolve (id, texto) ou None."""
        if cat is None:
            return None
        with self.trava:
            if not frio and self.rnd.random() < self.pular:
                return None
            vistos = self.recentes[robo]
            opcoes = [(i, f) for i, c, f in ids() if c == cat and i not in vistos]
            if not opcoes and cat != "geral":
                opcoes = [(i, f) for i, c, f in ids() if c == "geral" and i not in vistos]
            if not opcoes:
                return None
            escolha = self.rnd.choice(opcoes)
            vistos.append(escolha[0])
            return escolha
