#!/usr/bin/env python3
"""Calcula o menor cubo que guarda os componentes. É a conta de pré-CAD: a F4 confirma com o modelo 3D.

Uso:  python3 cad/caixa_minima.py [--parede 2.4]
Só biblioteca padrão do Python. As medidas vêm de cad/parametros.py (várias são NC: meça antes).

Arranjo assumido, de baixo para cima: pés, base com a grade do falante, falante virado para baixo,
amplificador deitado, XIAO deitado com o USB-C na parede de trás, botão sob o topo.
O microfone fica em pé, colado por dentro na parede da frente. Fios soldados direto, sem barra de pinos.
"""
import argparse
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import parametros as P  # noqa: E402


def cubo(falante, bateria=None, parede=P.PAREDE):
    f = P.FOLGA
    lado = {  # largura e profundidade internas: vale a maior
        "falante + folga + anel": falante.d + 2 * f + 2 * P.ANEL_FALANTE,
        "XIAO + microfone na parede da frente + fios": P.XIAO.placa[0] + P.MIC.espessura + P.FIOS + 2 * f,
        "placa mais larga + fios dos dois lados": max(P.XIAO.placa[1], P.AMP.placa[1]) + 2 * P.FIOS + 2 * f,
    }
    if bateria:
        lado["bateria deitada"] = bateria.comp + 2 * f
    altura = [  # pilha, de baixo para cima: vale a soma
        ("pés (saída do som)", P.PES),
        ("base", parede),
        ("falante", falante.altura),
        ("vão sobre o falante", P.VAO_FALANTE),
        ("amplificador + fios", P.AMP.placa[2] + P.FIOS),
        ("XIAO + fios", P.XIAO.altura + P.FIOS),
    ]
    if bateria:
        altura.append(("bateria + vão", bateria.esp + bateria.vao))
    altura += [("botão", P.BOTAO.altura), ("topo", parede)]

    interno = max(lado.values())
    largura = interno + 2 * parede
    alto = sum(v for _, v in altura)
    minimo = max(largura, alto)
    return {
        "lado": lado, "altura": altura, "interno": interno, "largura": largura, "alto": alto,
        "minimo": minimo, "alvo": math.ceil(minimo + P.MARGEM_NC),
        "manda": "altura" if alto >= largura else "largura",
    }


def mostrar(nome, r):
    print(f"\n== {nome}")
    for k, v in r["lado"].items():
        print(f"  lado interno  {v:5.1f}  {k}")
    print(f"  largura externa = {r['interno']:.1f} + 2 paredes = {r['largura']:.1f}")
    for k, v in r["altura"]:
        print(f"  altura        {v:5.1f}  {k}")
    print(f"  altura externa = {r['alto']:.1f}")
    print(f"  MÍNIMO = {r['minimo']:.1f} mm (manda a {r['manda']})  |  ALVO = {r['alvo']} mm "
          f"(mínimo + {P.MARGEM_NC} de margem, arredondado para cima)")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--parede", type=float, default=P.PAREDE, help="espessura da parede em mm (padrão %(default)s)")
    a = ap.parse_args()
    variantes = [
        ("A  padrão: USB-C, falante de 28 mm", P.FALANTE_28, None),
        ("B  com bateria 502030, falante de 28 mm", P.FALANTE_28, P.BATERIA_502030),
        ("C  USB-C, falante de 40 mm", P.FALANTE_40, None),
    ]
    print(f"Cubo mínimo (mm), parede {a.parede}. Medidas NC em cad/parametros.py ainda não foram medidas.")
    for nome, fal, bat in variantes:
        mostrar(nome, cubo(fal, bat, a.parede))
    lado = cubo(P.FALANTE_28, None, a.parede)["alvo"]
    gramas = (lado ** 3 - (lado - 2 * a.parede) ** 3) / 1000 * 1.24   # 6 paredes maciças, PLA 1,24 g/cm³
    print(f"\nPLA do cubo de {lado} mm (6 paredes maciças): {gramas:.0f} g (estimativa por volume, sem fatiador)")


if __name__ == "__main__":
    main()
