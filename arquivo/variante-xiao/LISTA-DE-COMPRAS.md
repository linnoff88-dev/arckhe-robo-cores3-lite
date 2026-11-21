# Lista de compras — robô ESP32 que só fala (fase 1)

> **Arquivado em 15/11/2026.** O projeto trocou para a placa pronta M5Stack CoreS3 Lite (ver `../../DEFINICAO.md`).
> Este arquivo descreve a variante antiga, XIAO ESP32S3 soldada num cubo impresso de 40 mm. Só referência.

Tudo o que você precisa comprar para o robô gravar a sua fala e tocar a resposta, dentro de um cubo de 40 mm.
A escolha de cada peça está explicada na [DEFINICAO.md](DEFINICAO.md).

## Como ler a lista

- **Usa / comprar:** o primeiro número é o que o robô usa; o segundo é o que você compra.
- **Os preços estão em reais (R$)** e os links abrem a busca do Mercado Livre do Brasil. O nome de cada item é o link.
- **Preço estimado é estimativa, não conferida.** Nenhum preço desta página foi lido em loja em 14/11/2026.
  A faixa serve para você saber a ordem de grandeza. Confira no anúncio antes de comprar.
- **NC** = medida não confirmada. A caixa foi calculada com o valor mais comum daquela peça. Meça a sua com o
  paquímetro e corrija em `cad/parametros.py` antes de imprimir.

## Riscos antes de comprar

- Nada foi comprado, soldado nem impresso. As ligações saíram das páginas dos fabricantes, não da bancada.
- A XIAO ESP32S3 tem de ser a versão **sem "Sense"** e tem de vir **com a antena**. Sem a antena o Wi-Fi fica fraco.
- O módulo MAX98357A genérico pode ter tamanho e pinos em ordem diferente do módulo da Adafruit, que é o da medida lida.
- O falante de 28 mm existe em várias alturas. A caixa reserva 10 mm. Um falante mais alto pede um cubo maior.
- A compra da XIAO ESP32S3 no Brasil não foi conferida. Se não achar, veja a alternativa no fim desta página.
- O cubo de 40 mm só fecha com os fios soldados direto nas placas. Com barra de pinos e fios de encaixe, não fecha.

## Quanto custa

- Peças da fase 1 (itens 1 a 7): **R$ 158–370** (estimativa, não conferida).
- Com o cabo e a fonte USB, se você não tiver (itens 8 e 9): **R$ 193–460** (estimativa, não conferida).
- Filamento: cerca de 22 g de PLA (estimativa por volume). Sai do rolo que você já tem.

## Fase 1: o que comprar

### Eletrônica

| # | Item (o nome abre a busca) | Usa / comprar | Para que serve | Preço estimado (não conferido) |
|---|---|---|---|---|
| 1 | [Seeed Studio XIAO ESP32S3 (sem "Sense"), com antena](https://lista.mercadolivre.com.br/seeed-studio-xiao-esp32s3) | 1 / 1 | Cérebro do robô: lê o botão, grava, fala com o servidor por Wi-Fi e toca. 21 × 17,8 mm, 8 MB de PSRAM. NC: altura da placa (4,5 mm), quanto o USB-C passa da borda (1,5 mm), tamanho da antena. | R$ 90–180 |
| 2 | [Microfone I²S INMP441 (módulo)](https://lista.mercadolivre.com.br/microfone-inmp441-i2s) | 1 / 1 | O ouvido. Microfone digital, ligado por 3 fios de sinal. NC: diâmetro (14 mm), espessura (3,5 mm) e de que lado fica o furo do som. | R$ 15–40 |
| 3 | [Amplificador I²S MAX98357A (módulo)](https://lista.mercadolivre.com.br/amplificador-max98357a-i2s) | 1 / 1 | A boca: recebe o áudio digital e move o falante. Módulo da Adafruit: 19,4 × 17,8 × 3,0 mm. NC no módulo genérico: tamanho e ordem dos pinos. | R$ 15–40 |
| 4 | [Alto-falante de 28 mm, 8 Ω, 2 W](https://lista.mercadolivre.com.br/alto-falante-28mm-8-ohms-2w) | 1 / 1 | Toca a voz. Fica virado para baixo, sobre a grade da base. NC: altura (10 mm reservados). | R$ 8–25 |
| 5 | [Chave táctil 6 × 6 × 5 mm](https://lista.mercadolivre.com.br/chave-tactil-6x6x5mm) | 1 / 1 pacote de 10 | O botão de falar, sob a tecla do topo. NC: altura total (5 mm). | R$ 5–15 (pacote) |
| 6 | [Fio flexível de silicone 28 ou 30 AWG, várias cores](https://lista.mercadolivre.com.br/fio-silicone-30awg-cores) | cerca de 1 m / 1 kit | Liga as placas: 12 fios de 6 a 8 cm, soldados direto, sem barra de pinos. | R$ 15–40 (kit) |
| 7 | [Parafuso M2 × 8 autoatarraxante](https://lista.mercadolivre.com.br/parafuso-m2x8-autoatarraxante) | 4 / 1 kit | Fecha a base na casca, por baixo. NC: o fecho pode virar encaixe quando a caixa for desenhada. | R$ 10–30 (kit) |

### Cabo e fonte (você talvez já tenha)

| # | Item (o nome abre a busca) | Usa / comprar | Para que serve | Preço estimado (não conferido) |
|---|---|---|---|---|
| 8 | [Cabo USB-C de dados](https://lista.mercadolivre.com.br/cabo-usb-c-dados) | 1 / 1 | Grava o programa e alimenta o robô. Tem de ser de dados: cabo só de carga não grava. NC: ponta do plugue (abertura de 9,5 × 3,8 mm) e corpo do plugue (rebaixo de 12,5 × 7 mm). | R$ 15–40 |
| 9 | [Fonte USB de 5 V, 1 A ou mais](https://lista.mercadolivre.com.br/fonte-usb-5v-2a) | 1 / 1 | Alimenta o robô na mesa. Carregador de celular serve. | R$ 20–50 |

### Ferramentas (você provavelmente já tem)

Ferro de solda de ponta fina, estanho, alicate de corte, pinça, multímetro e paquímetro.

## Não comprar agora (opcionais, fora da fase 1)

| Item (o nome abre a busca) | Para quê | Efeito no cubo | Preço estimado (não conferido) |
|---|---|---|---|
| [Bateria LiPo 3,7 V 250 mAh, modelo 502030, com proteção](https://lista.mercadolivre.com.br/bateria-lipo-3.7v-250mah-502030) | Tirar o robô do cabo. A XIAO já carrega a bateria. NC: 5 × 20 × 30 mm. | 40 → 46 mm | R$ 20–50 |
| [Alto-falante de 40 mm, 4 Ω, 3 W](https://lista.mercadolivre.com.br/alto-falante-40mm-4-ohms-3w) | Voz mais cheia. NC: altura (20 mm). | 40 → 50 mm | R$ 12–35 |
| [LED RGB endereçável WS2812B](https://lista.mercadolivre.com.br/led-ws2812b-rgb) | "Olhos" que mudam de cor com o estado. | nenhum | R$ 5–20 |
| [Tela OLED 0,96" I²C SSD1306](https://lista.mercadolivre.com.br/display-oled-0.96-i2c-ssd1306) | Rosto com olhos desenhados. NC: tamanho do módulo. | a conferir | R$ 20–45 |

## Alternativas de placa

| Se… | Compre no lugar | O que muda |
|---|---|---|
| Não achar a XIAO ESP32S3 | [Seeed Studio XIAO ESP32S3 Sense](https://lista.mercadolivre.com.br/seeed-studio-xiao-esp32s3-sense) | Já traz o microfone: o item 2 sai. O furo do microfone muda de lugar e a placa fica com 15 mm de altura. |
| Quiser pular a solda e a caixa | [M5Stack Atom Echo](https://lista.mercadolivre.com.br/m5stack-atom-echo) | Cubo pronto de 24 mm com microfone, falante e botão. Falante de 0,8 W e sem PSRAM na ficha. Os itens 1 a 7 saem. Decisão do Nei: veja a seção 5 da DEFINICAO.md. |
