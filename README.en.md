# robo-cores3-lite

[![Talking robot](guia/assets/banner-en.jpg)](https://inematds.github.io/robo-cores3-lite/guia/en/)

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

🎬 Video: https://www.youtube.com/watch?v=ckhcNbClXNs

## What it is

This is an open project for building a tabletop robot that talks by voice: you hold your finger on the screen, speak, and it replies aloud, with the text on screen. It can also look through its camera. Its body is a ready-made board, the M5Stack CoreS3 Lite (a 5 cm square with a screen, camera, microphones, and speaker, with no soldering). Its “brain” runs through your computer: it transcribes speech and generates the voice right there, then asks Claude for an answer through your subscription, with no charge per question. The server is ready and its performance has been measured; the board has not arrived yet, so the complete robot has not been tested.

## 📖 User guide

Full guide (landing page + step-by-step instructions): **https://inematds.github.io/robo-cores3-lite/guia/en/**

## More details

A square, stationary tabletop robot built with the **M5Stack CoreS3 Lite**: it listens, replies by voice, displays a face and text on screen, and sees through its camera. The board comes ready to use, with no soldering.

Two “brain” options:
- **Option B (default): local server** on this machine. Whisper → `claude -p` through the subscription → Chatterbox. No cost per question (uses the Claude subscription).
- **Option A: direct connection to an API** for real-time voice (Gemini Live or OpenAI Realtime). Design only: nothing is called without Nei’s authorization (Nei Maldaner, project author).

**Status on 15/11/2026: Option B server ready (F1); the board hasn’t arrived yet.** With the response streamed in parts, the first sound starts in 6.8 to 7.6 s, and a waiting phrase (“let me check the clock…”) fills the silence; 19 s for the first response after 10 minutes idle; the photo feature also works. The firmware is a skeleton that compiles and displays the PSRAM.

| For | Where |
|---|---|
| Understand what it is and what has been decided | [DEFINICAO.md](DEFINICAO.md) (in Portuguese) |
| Buying | [LISTA-DE-COMPRAS.md](LISTA-DE-COMPRAS.md) (in Portuguese) |
| Phases and each phase’s completion criteria | [PLANO.md](PLANO.md) (in Portuguese) |
| Local server (Option B) | [servidor/README.md](servidor/README.md) |
| Board program | [firmware/README.md](firmware/README.md) |
| Questions and limitations (API, boards, camera, movement) | [FAQ.md](FAQ.md) (in Portuguese) |
| Previous version (XIAO soldered into a 40 mm cube) | [arquivo/variante-xiao/](arquivo/variante-xiao/DEFINICAO.md) (in Portuguese) |
| Resume the work | [handoffs/latest.md](handoffs/latest.md) (in Portuguese) |

## In numbers

- Board: 54 × 54 × 16.5 mm, 54 g. 2" screen, 320 × 240, with touch. 0.3 MP camera. 200 mAh battery.
- Price: R$ 256.55 at the official M5Stack AliExpress store (checked on 15/11/2026, excluding shipping and taxes).
- Audio: 16 kHz, 16 bits, mono, in both directions. Speech up to 15 s.
- Option B, measured on 15/11: first sound in 6.8 to 7.6 s with the response streamed in parts (warm), 19 s from touch in the cold case. Details in [servidor/MEDIDAS.md](servidor/MEDIDAS.md) (in Portuguese).

## The process, from start to finish

Legend: 🧠 session with Nei · ⚙️ command/script · 🤖 `claude -p`

| # | Step | Command | Who | Exists today? |
|---|---|---|---|---|
| 1 | Read the definition and choose a voice and option | [DEFINICAO.md](DEFINICAO.md) (in Portuguese), section 3 | 🧠 | yes |
| 2 | Buy the CoreS3 Lite | [LISTA-DE-COMPRAS.md](LISTA-DE-COMPRAS.md) (in Portuguese) | 🧠 | yes |
| 3 | Copy the server `.env` and choose the token | `cp servidor/env.exemplo servidor/.env` | 🧠 | yes |
| 4 | Start the server (Option B); it loads Whisper and the voice engine and keeps them resident | `python3 servidor/servidor.py` | ⚙️ | yes |
| 5 | Test the server without the robot, with and without a photo | `python3 servidor/testar.py servidor/teste/pergunta.wav` (and `--foto`, `--limites`) | ⚙️ | yes |
| 5b | Record the waiting phrases in the robot’s voice (once, or when changing the voice) | `python3 servidor/gerar_espera.py` | ⚙️ | yes (32 phrases) |
| 6 | During each turn: write the response | `claude -p --model haiku --tools "" --strict-mcp-config --no-session-persistence …` | 🤖 | command tested |
| 7 | Install the board libraries (notify Nei) | `arduino-cli lib install M5Unified M5GFX` | ⚙️ | no: phase F2 |
| 8 | Fill in Wi-Fi, server, token, and brain settings | `cp firmware/robo_fala/segredos.exemplo.h firmware/robo_fala/segredos.h` | 🧠 | yes |
| 9 | Compile the firmware | `arduino-cli compile --fqbn esp32:esp32:m5stack_cores3 firmware/robo_fala` | ⚙️ | yes (skeleton) |
| 10 | Upload to the board | `arduino-cli upload --fqbn esp32:esp32:m5stack_cores3 -p /dev/ttyACM0 firmware/robo_fala` | ⚙️ | not tested: no board |
| 11 | Talk at the workbench: 5 consecutive questions | [PLANO.md](PLANO.md) (in Portuguese), phase F2 | 🧠 | — |
| 12 | Option A, direct API connection | only with Nei’s authorization: [PLANO.md](PLANO.md) (in Portuguese), phase F3 | 🧠 | — |
| 13 | Vision: photo and a few frames | [PLANO.md](PLANO.md) (in Portuguese), phase F4 | 🧠 | — |
| 14 | PT/EN/ES guide in `guia/` (skill `projetos-landing-guia`, translation via `inema-traduz`, independent reviewer) | `guia/index.html`, `guia/en/`, `guia/es/` | 🧠 + 🤖 | yes (15/11/2026) |
| 15 | Publish: push to `main`; GitHub Pages is published through Actions | `git push` → https://inematds.github.io/robo-cores3-lite/guia/ | ⚙️ | yes |
| 16 | inema.club portal, inemabuscas, and PRO catalog | skill `atualiza-portal` | 🧠 | yes — [PUBLICACAO.md](PUBLICACAO.md) (in Portuguese) |
| 17 | Topic in the INEMA.ROBOT Telegram group + MENU | skill `postar-telegram` | 🧠 | yes — [PUBLICACAO.md](PUBLICACAO.md) (in Portuguese) |
| 18 | Video on the lives6 channel and in the guide | another agent; `<!-- VIDEO: -->` marker in the guide | 🧠 | yes (15/11/2026) — [lives6](https://www.youtube.com/watch?v=ckhcNbClXNs) |

In the robot, the only step that uses `claude -p` is step 6, through the subscription, with no tools. The 🤖 in step 14 is the translation and reviewer.

## Rules

- No external API without Nei’s explicit authorization (service and purpose). Option A exists only on paper.
- Claude only through the subscription (`claude -p`), never with an API key.
- Public repo at https://github.com/inematds/robo-cores3-lite (published at Nei’s direction on 15/11/2026).