"""Medidas do robô, em mm. Fonte única: DEFINICAO.md e LISTA-DE-COMPRAS.md citam estes números.

Fonte de cada medida:
  "P"  = página ou ficha do fabricante, lida em 14/11/2026 (URLs na DEFINICAO.md, seção Fontes)
  "T"  = loja ou terceiro
  "NC" = não confirmado em fonte lida. É o valor usual de mercado: MEÇA a sua peça com paquímetro
         e corrija aqui antes de desenhar ou imprimir a parte que encosta nela.

Na F4 (caixa), as seções IMPRESSORA, FOLGAS e IMPRESSAO_LIMITES do robos-impressos entram neste arquivo
(veja cad/README.md).
"""
from types import SimpleNamespace as NS

# ---------------------------------------------------------------- caixa
PAREDE = 2.0          # parede mínima do projeto (mesma regra do robos-impressos); 2,4 = 6 passadas de 0,4
FOLGA = 0.5           # folga por lado entre componente e plástico
FIOS = 3.0            # NC: altura reservada para solda e fio dobrado sobre cada placa
ANEL_FALANTE = 1.2    # largura do anel impresso que segura o falante pela borda
VAO_FALANTE = 1.5     # vão entre o fundo do falante e a primeira placa (ímã não encosta em solda)
PES = 3.0             # altura dos pés: o som sai por baixo, pelo vão entre a base e a mesa
MARGEM_NC = 2.5       # margem somada ao mínimo calculado enquanto houver medida NC

# ---------------------------------------------------------------- componentes
XIAO = NS(                                # Seeed Studio XIAO ESP32S3 (sem "Sense")
    placa=(21.0, 17.8),                   # P (wiki da Seeed): comprimento x largura
    altura=4.5,                           # NC: placa de 1 face + conector USB-C, sem barra de pinos
    usb_passa_da_borda=1.5,               # NC: quanto o conector USB-C passa da borda da placa
    psram_mb=8, flash_mb=8,               # P
)
ANTENA = NS(                              # antena flexível que vem com o XIAO (conector U.FL)
    tamanho=(40.0, 8.0),                  # NC: não lido em fonte; cola numa parede interna
)
AMP = NS(                                 # amplificador I2S MAX98357A
    placa=(19.4, 17.8, 3.0),              # P (Adafruit 3006). Módulo genérico: NC, meça
)
MIC = NS(                                 # microfone I2S INMP441, módulo redondo
    diametro=14.0,                        # NC
    espessura=3.5,                        # NC: placa + chip + solda dos fios
    furo_do_som="NC",                     # NC: conferir de que lado da placa fica o furo acústico
)
FALANTE_28 = NS(d=28.0, altura=10.0)      # T (diâmetro do anúncio) / NC (altura): 8 ohms, 2 W
FALANTE_40 = NS(d=40.0, altura=20.0)      # T (diâmetro do anúncio) / NC (altura): 4 ohms, 3 W
BOTAO = NS(corpo=(6.0, 6.0), altura=5.0)  # T (nome do anúncio "6x6x5") / NC
BATERIA_502030 = NS(                      # LiPo 1S 3,7 V ~250 mAh. Opcional, fora da fase 1
    esp=5.0, larg=20.0, comp=30.0,        # NC: lido do código do modelo (50-20-30), não de uma ficha
    vao=1.5,                              # espaço para a bateria não ser apertada
)
PLUGUE_USB_C = NS(
    corpo=(12.5, 7.0),                    # NC: corpo plástico do plugue do cabo (rebaixo na parede)
    abertura=(9.5, 3.8),                  # NC: passagem da ponta metálica do plugue, com folga
)
