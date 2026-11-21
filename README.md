# robo-cores3-lite

<div align="center">
  <img src="capa/logo.svg" alt="Arckhé AI" height="48" />
  <p><strong>Arckhé AI</strong></p>
</div>


[![RobÃ´ que conversa](guia/assets/banner.jpg)](https://inematds.github.io/robo-cores3-lite/guia/)

**ðŸ‡§ðŸ‡· [PortuguÃªs](README.md) Â· ðŸ‡ºðŸ‡¸ [English](README.en.md) Â· ðŸ‡ªðŸ‡¸ [EspaÃ±ol](README.es.md)**

ðŸŽ¬ VÃ­deo: https://www.youtube.com/watch?v=ckhcNbClXNs

## O que Ã©

Este Ã© um projeto aberto para montar um robÃ´ de mesa que conversa por voz: vocÃª segura o dedo na tela, fala, e ele
responde em voz alta, com o texto na tela, e pode olhar pela cÃ¢mera. O corpo Ã© uma placa pronta, a M5Stack CoreS3
Lite (um quadrado de 5 cm com tela, cÃ¢mera, microfones e alto-falante, sem solda). O "cÃ©rebro" passa pelo seu
computador: ele transcreve e gera a voz ali mesmo e pede a resposta ao Claude pela sua assinatura, sem pagar por
pergunta. Hoje esse servidor estÃ¡ pronto e medido; a placa ainda nÃ£o chegou,
entÃ£o o robÃ´ inteiro ainda nÃ£o foi testado.

## ðŸ“– Guia de uso

Guia completo (landing + passo a passo): **https://inematds.github.io/robo-cores3-lite/guia/**

## Mais detalhes

Um robÃ´ de mesa quadrado, sem movimento, feito com a **M5Stack CoreS3 Lite**: ele ouve, responde com voz, mostra um
rosto e o texto na tela, e enxerga pela cÃ¢mera. A placa jÃ¡ vem pronta, sem solda.

Duas opÃ§Ãµes de "cÃ©rebro":
- **OpÃ§Ã£o B (padrÃ£o): servidor local** nesta mÃ¡quina. Whisper â†’ `claude -p` pela assinatura â†’ Chatterbox. Sem custo por pergunta (usa a assinatura do Claude).
- **OpÃ§Ã£o A: direto numa API** de voz em tempo real (Gemini Live ou OpenAI Realtime). SÃ³ desenho: nada Ã© chamado sem
  autorizaÃ§Ã£o do Nei (Nei Maldaner, autor do projeto).

**Estado em 15/11/2026: servidor da opÃ§Ã£o B pronto (F1), placa ainda nÃ£o chegou.** Com a resposta por partes, o
primeiro som sai em 6,8 a 7,6 s, e uma frase de espera ("deixa eu ver o relÃ³gioâ€¦") cobre o silÃªncio; 19 s na
primeira depois de 10 min parado; a foto tambÃ©m funciona. O firmware Ã© um esqueleto
que compila e mostra a PSRAM.

| Para | Onde |
|---|---|
| Entender o que Ã© e o que foi decidido | [DEFINICAO.md](DEFINICAO.md) |
| Comprar | [LISTA-DE-COMPRAS.md](LISTA-DE-COMPRAS.md) |
| Fases e critÃ©rio de pronto de cada uma | [PLANO.md](PLANO.md) |
| Servidor local (opÃ§Ã£o B) | [servidor/README.md](servidor/README.md) |
| Programa da placa | [firmware/README.md](firmware/README.md) |
| Perguntas e limites (API, placas, cÃ¢mera, movimento) | [FAQ.md](FAQ.md) |
| Ideias: a placa como cabeÃ§a de outros robÃ´s (6 exemplos ilustrados) | [IDEIAS-CORPOS.md](IDEIAS-CORPOS.md) |
| VersÃ£o anterior (XIAO soldada num cubo de 40 mm) | [arquivo/variante-xiao/](arquivo/variante-xiao/DEFINICAO.md) |
| Retomar o trabalho | [handoffs/latest.md](handoffs/latest.md) |

## Em nÃºmeros

- Placa: 54 Ã— 54 Ã— 16,5 mm, 54 g. Tela de 2", 320 Ã— 240, com toque. CÃ¢mera de 0,3 MP. Bateria de 200 mAh.
- PreÃ§o: R$ 256,55 na loja oficial M5Stack do AliExpress (lido em 15/11/2026, sem frete nem imposto).
- Ãudio: 16 kHz, 16 bits, mono, nos dois sentidos. Fala de atÃ© 15 s.
- OpÃ§Ã£o B, medido em 15/11: primeiro som em 6,8 a 7,6 s com a resposta por partes (quente), 19 s do toque no caso frio. Detalhe em [servidor/MEDIDAS.md](servidor/MEDIDAS.md).

## O processo, do inÃ­cio ao fim

Legenda: ðŸ§  sessÃ£o com o Nei Â· âš™ï¸ comando/script Â· ðŸ¤– `claude -p`

| # | Passo | Comando | Quem | Existe hoje? |
|---|---|---|---|---|
| 1 | Ler a definiÃ§Ã£o e escolher voz e opÃ§Ã£o | [DEFINICAO.md](DEFINICAO.md), seÃ§Ã£o 3 | ðŸ§  | sim |
| 2 | Comprar a CoreS3 Lite | [LISTA-DE-COMPRAS.md](LISTA-DE-COMPRAS.md) | ðŸ§  | sim |
| 3 | Copiar o `.env` do servidor e escolher o token | `cp servidor/env.exemplo servidor/.env` | ðŸ§  | sim |
| 4 | Subir o servidor (opÃ§Ã£o B); ele sobe o Whisper e a voz residentes. Fica desligado; ligar sÃ³ quando for usar o robÃ´ (unidade em `servidor/robo-servidor.service`, instalada em `~/.config/systemd/user/`) | `systemctl --user start robo-servidor` (ou `python3 servidor/servidor.py`); parar: `systemctl --user stop robo-servidor` | âš™ï¸ | sim |
| 5 | Testar o servidor sem o robÃ´, com e sem foto | `python3 servidor/testar.py servidor/teste/pergunta.wav` (e `--foto`, `--limites`) | âš™ï¸ | sim |
| 5b | Gravar as frases de espera na voz do robÃ´ (sÃ³ uma vez, ou ao trocar a voz) | `python3 servidor/gerar_espera.py` | âš™ï¸ | sim (32 frases) |
| 6 | Dentro de cada turno: escrever a resposta | `claude -p --model haiku --tools "" --strict-mcp-config --no-session-persistence â€¦` | ðŸ¤– | comando testado |
| 7 | Instalar as bibliotecas da placa (avisar o Nei) | `arduino-cli lib install M5Unified M5GFX` | âš™ï¸ | nÃ£o: fase F2 |
| 8 | Preencher Wi-Fi, servidor, token e cÃ©rebro | `cp firmware/robo_fala/segredos.exemplo.h firmware/robo_fala/segredos.h` | ðŸ§  | sim |
| 9 | Compilar o firmware | `arduino-cli compile --fqbn esp32:esp32:m5stack_cores3 firmware/robo_fala` | âš™ï¸ | sim (esqueleto) |
| 10 | Gravar na placa | `arduino-cli upload --fqbn esp32:esp32:m5stack_cores3 -p /dev/ttyACM0 firmware/robo_fala` | âš™ï¸ | nÃ£o testado: sem placa |
| 11 | Conversar na bancada: 5 perguntas seguidas | [PLANO.md](PLANO.md), fase F2 | ðŸ§  | â€” |
| 12 | OpÃ§Ã£o A, direto na API | sÃ³ com autorizaÃ§Ã£o do Nei: [PLANO.md](PLANO.md), fase F3 | ðŸ§  | â€” |
| 13 | VisÃ£o: foto e poucos quadros | [PLANO.md](PLANO.md), fase F4 | ðŸ§  | â€” |
| 14 | Guia PT/EN/ES em `guia/` (skill `projetos-landing-guia`, traduÃ§Ã£o pelo `inema-traduz`, revisor independente) | `guia/index.html`, `guia/en/`, `guia/es/` | ðŸ§  + ðŸ¤– | sim (15/11/2026) |
| 15 | Publicar: push no `main`; o GitHub Pages sai pelo Actions | `git push` â†’ https://inematds.github.io/robo-cores3-lite/guia/ | âš™ï¸ | sim |
| 16 | Portal inema.club, inemabuscas e catÃ¡logo PRO | skill `atualiza-portal` | ðŸ§  | sim â€” [PUBLICACAO.md](PUBLICACAO.md) |
| 17 | TÃ³pico no grupo INEMA.ROBOT do Telegram + MENU | skill `postar-telegram` | ðŸ§  | sim â€” [PUBLICACAO.md](PUBLICACAO.md) |
| 18 | VÃ­deo no canal lives6 e no guia | outro agente; marca `<!-- VIDEO: -->` no guia | ðŸ§  | sim (15/11/2026) â€” [lives6](https://www.youtube.com/watch?v=ckhcNbClXNs) |

No robÃ´, o Ãºnico passo com `claude -p` Ã© o 6, pela assinatura, sem ferramentas. O ðŸ¤– do passo 14 Ã© a traduÃ§Ã£o e o revisor.

## Regras

- Nenhuma API externa sem autorizaÃ§Ã£o explÃ­cita do Nei (serviÃ§o e finalidade). A opÃ§Ã£o A existe sÃ³ no papel.
- Claude sÃ³ pela assinatura (`claude -p`), nunca por chave de API.
- Repo pÃºblico em https://github.com/inematds/robo-cores3-lite (publicado por ordem do Nei em 15/11/2026).

---

<div align="center">
  <img src="capa/logo.svg" alt="Arckhé AI" height="32" />
  <p><strong>Arckhé AI</strong></p>
</div>