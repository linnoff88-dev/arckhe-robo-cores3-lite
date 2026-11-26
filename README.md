ï»¿# robo-cores3-lite

<div align="center">
  <img src="capa/logo.svg" alt="Arckhé AI" height="48" />
  <p><strong>Arckhé AI</strong></p>
</div>


[![RobêÂ´ que conversa](guia/assets/banner.jpg)](https://inematds.github.io/robo-cores3-lite/guia/)

**ê°Å¸â¡Â§ê°Å¸â¡Â· [PortuguêÂªs](README.md) êÂ· ê°Å¸â¡Âºê°Å¸â¡Â¸ [English](README.en.md) êÂ· ê°Å¸â¡Âªê°Å¸â¡Â¸ [EspaêÂ±ol](README.es.md)**

ê°Å¸Å½Â¬ VêÂ­deo: https://www.youtube.com/watch?v=ckhcNbClXNs

## O que êÂ©

Este êÂ© um projeto aberto para montar um robêÂ´ de mesa que conversa por voz: vocêÂª segura o dedo na tela, fala, e ele
responde em voz alta, com o texto na tela, e pode olhar pela cêÂ¢mera. O corpo êÂ© uma placa pronta, a M5Stack CoreS3
Lite (um quadrado de 5 cm com tela, cêÂ¢mera, microfones e alto-falante, sem solda). O "cêÂ©rebro" passa pelo seu
computador: ele transcreve e gera a voz ali mesmo e pede a resposta ao Claude pela sua assinatura, sem pagar por
pergunta. Hoje esse servidor estêÂ¡ pronto e medido; a placa ainda nêÂ£o chegou,
entêÂ£o o robêÂ´ inteiro ainda nêÂ£o foi testado.

## ê°Å¸ââ Guia de uso

Guia completo (landing + passo a passo): **https://inematds.github.io/robo-cores3-lite/guia/**

## Mais detalhes

Um robêÂ´ de mesa quadrado, sem movimento, feito com a **M5Stack CoreS3 Lite**: ele ouve, responde com voz, mostra um
rosto e o texto na tela, e enxerga pela cêÂ¢mera. A placa jêÂ¡ vem pronta, sem solda.

Duas opêÂ§êÂµes de "cêÂ©rebro":
- **OpêÂ§êÂ£o B (padrêÂ£o): servidor local** nesta mêÂ¡quina. Whisper ê¢â â `claude -p` pela assinatura ê¢â â Chatterbox. Sem custo por pergunta (usa a assinatura do Claude).
- **OpêÂ§êÂ£o A: direto numa API** de voz em tempo real (Gemini Live ou OpenAI Realtime). SêÂ³ desenho: nada êÂ© chamado sem
  autorizaêÂ§êÂ£o do Nei (Nei Maldaner, autor do projeto).

**Estado em 15/11/2026: servidor da opêÂ§êÂ£o B pronto (F1), placa ainda nêÂ£o chegou.** Com a resposta por partes, o
primeiro som sai em 6,8 a 7,6 s, e uma frase de espera ("deixa eu ver o relêÂ³gioê¢â¬Â¦") cobre o silêÂªncio; 19 s na
primeira depois de 10 min parado; a foto tambêÂ©m funciona. O firmware êÂ© um esqueleto
que compila e mostra a PSRAM.

| Para | Onde |
|---|---|
| Entender o que êÂ© e o que foi decidido | [DEFINICAO.md](DEFINICAO.md) |
| Comprar | [LISTA-DE-COMPRAS.md](LISTA-DE-COMPRAS.md) |
| Fases e critêÂ©rio de pronto de cada uma | [PLANO.md](PLANO.md) |
| Servidor local (opêÂ§êÂ£o B) | [servidor/README.md](servidor/README.md) |
| Programa da placa | [firmware/README.md](firmware/README.md) |
| Perguntas e limites (API, placas, cêÂ¢mera, movimento) | [FAQ.md](FAQ.md) |
| Ideias: a placa como cabeêÂ§a de outros robêÂ´s (6 exemplos ilustrados) | [IDEIAS-CORPOS.md](IDEIAS-CORPOS.md) |
| VersêÂ£o anterior (XIAO soldada num cubo de 40 mm) | [arquivo/variante-xiao/](arquivo/variante-xiao/DEFINICAO.md) |
| Retomar o trabalho | [handoffs/latest.md](handoffs/latest.md) |

## Em nêÂºmeros

- Placa: 54 êâ 54 êâ 16,5 mm, 54 g. Tela de 2", 320 êâ 240, com toque. CêÂ¢mera de 0,3 MP. Bateria de 200 mAh.
- PreêÂ§o: R$ 256,55 na loja oficial M5Stack do AliExpress (lido em 15/11/2026, sem frete nem imposto).
- êÂudio: 16 kHz, 16 bits, mono, nos dois sentidos. Fala de atêÂ© 15 s.
- OpêÂ§êÂ£o B, medido em 15/11: primeiro som em 6,8 a 7,6 s com a resposta por partes (quente), 19 s do toque no caso frio. Detalhe em [servidor/MEDIDAS.md](servidor/MEDIDAS.md).

## O processo, do inêÂ­cio ao fim

Legenda: ê°Å¸Â§Â  sessêÂ£o com o Nei êÂ· ê¢Å¡â¢ê¯Â¸Â comando/script êÂ· ê°Å¸Â¤â `claude -p`

| # | Passo | Comando | Quem | Existe hoje? |
|---|---|---|---|---|
| 1 | Ler a definiêÂ§êÂ£o e escolher voz e opêÂ§êÂ£o | [DEFINICAO.md](DEFINICAO.md), seêÂ§êÂ£o 3 | ê°Å¸Â§Â  | sim |
| 2 | Comprar a CoreS3 Lite | [LISTA-DE-COMPRAS.md](LISTA-DE-COMPRAS.md) | ê°Å¸Â§Â  | sim |
| 3 | Copiar o `.env` do servidor e escolher o token | `cp servidor/env.exemplo servidor/.env` | ê°Å¸Â§Â  | sim |
| 4 | Subir o servidor (opêÂ§êÂ£o B); ele sobe o Whisper e a voz residentes. Fica desligado; ligar sêÂ³ quando for usar o robêÂ´ (unidade em `servidor/robo-servidor.service`, instalada em `~/.config/systemd/user/`) | `systemctl --user start robo-servidor` (ou `python3 servidor/servidor.py`); parar: `systemctl --user stop robo-servidor` | ê¢Å¡â¢ê¯Â¸Â | sim |
| 5 | Testar o servidor sem o robêÂ´, com e sem foto | `python3 servidor/testar.py servidor/teste/pergunta.wav` (e `--foto`, `--limites`) | ê¢Å¡â¢ê¯Â¸Â | sim |
| 5b | Gravar as frases de espera na voz do robêÂ´ (sêÂ³ uma vez, ou ao trocar a voz) | `python3 servidor/gerar_espera.py` | ê¢Å¡â¢ê¯Â¸Â | sim (32 frases) |
| 6 | Dentro de cada turno: escrever a resposta | `claude -p --model haiku --tools "" --strict-mcp-config --no-session-persistence ê¢â¬Â¦` | ê°Å¸Â¤â | comando testado |
| 7 | Instalar as bibliotecas da placa (avisar o Nei) | `arduino-cli lib install M5Unified M5GFX` | ê¢Å¡â¢ê¯Â¸Â | nêÂ£o: fase F2 |
| 8 | Preencher Wi-Fi, servidor, token e cêÂ©rebro | `cp firmware/robo_fala/segredos.exemplo.h firmware/robo_fala/segredos.h` | ê°Å¸Â§Â  | sim |
| 9 | Compilar o firmware | `arduino-cli compile --fqbn esp32:esp32:m5stack_cores3 firmware/robo_fala` | ê¢Å¡â¢ê¯Â¸Â | sim (esqueleto) |
| 10 | Gravar na placa | `arduino-cli upload --fqbn esp32:esp32:m5stack_cores3 -p /dev/ttyACM0 firmware/robo_fala` | ê¢Å¡â¢ê¯Â¸Â | nêÂ£o testado: sem placa |
| 11 | Conversar na bancada: 5 perguntas seguidas | [PLANO.md](PLANO.md), fase F2 | ê°Å¸Â§Â  | ê¢â¬â |
| 12 | OpêÂ§êÂ£o A, direto na API | sêÂ³ com autorizaêÂ§êÂ£o do Nei: [PLANO.md](PLANO.md), fase F3 | ê°Å¸Â§Â  | ê¢â¬â |
| 13 | VisêÂ£o: foto e poucos quadros | [PLANO.md](PLANO.md), fase F4 | ê°Å¸Â§Â  | ê¢â¬â |
| 14 | Guia PT/EN/ES em `guia/` (skill `projetos-landing-guia`, traduêÂ§êÂ£o pelo `inema-traduz`, revisor independente) | `guia/index.html`, `guia/en/`, `guia/es/` | ê°Å¸Â§Â  + ê°Å¸Â¤â | sim (15/11/2026) |
| 15 | Publicar: push no `main`; o GitHub Pages sai pelo Actions | `git push` ê¢â â https://inematds.github.io/robo-cores3-lite/guia/ | ê¢Å¡â¢ê¯Â¸Â | sim |
| 16 | Portal inema.club, inemabuscas e catêÂ¡logo PRO | skill `atualiza-portal` | ê°Å¸Â§Â  | sim ê¢â¬â [PUBLICACAO.md](PUBLICACAO.md) |
| 17 | TêÂ³pico no grupo INEMA.ROBOT do Telegram + MENU | skill `postar-telegram` | ê°Å¸Â§Â  | sim ê¢â¬â [PUBLICACAO.md](PUBLICACAO.md) |
| 18 | VêÂ­deo no canal lives6 e no guia | outro agente; marca `<!-- VIDEO: -->` no guia | ê°Å¸Â§Â  | sim (15/11/2026) ê¢â¬â [lives6](https://www.youtube.com/watch?v=ckhcNbClXNs) |

No robêÂ´, o êÂºnico passo com `claude -p` êÂ© o 6, pela assinatura, sem ferramentas. O ê°Å¸Â¤â do passo 14 êÂ© a traduêÂ§êÂ£o e o revisor.

## Regras

- Nenhuma API externa sem autorizaêÂ§êÂ£o explêÂ­cita do Nei (serviêÂ§o e finalidade). A opêÂ§êÂ£o A existe sêÂ³ no papel.
- Claude sêÂ³ pela assinatura (`claude -p`), nunca por chave de API.
- Repo pêÂºblico em https://github.com/inematds/robo-cores3-lite (publicado por ordem do Nei em 15/11/2026).

---

<div align="center">
  <img src="capa/logo.svg" alt="Arckhé AI" height="32" />
  <p><strong>Arckhé AI</strong></p>
</div>