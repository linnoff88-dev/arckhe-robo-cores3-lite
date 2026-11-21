# robo-cores3-lite

[![Robot que conversa](guia/assets/banner-es.jpg)](https://inematds.github.io/robo-cores3-lite/guia/es/)

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

🎬 Video: https://www.youtube.com/watch?v=ckhcNbClXNs

## Qué es

Este es un proyecto abierto para armar un robot de escritorio que conversa por voz: mantienes el dedo en la pantalla, hablas y él responde en voz alta, muestra el texto en la pantalla y puede mirar por la cámara. El cuerpo es una placa lista para usar, la M5Stack CoreS3 Lite (un cuadrado de 5 cm con pantalla, cámara, micrófonos y altavoz, sin soldaduras). El «cerebro» pasa por tu computadora: transcribe y genera la voz allí mismo y le pide la respuesta a Claude con tu suscripción, sin pagar por pregunta. El servidor ya está listo y medido; la placa aún no llegó, así que el robot completo todavía no se ha probado.

## 📖 Guía de uso

Guía completa (landing + paso a paso): **https://inematds.github.io/robo-cores3-lite/guia/es/**

## Más detalles

Un robot de escritorio cuadrado, sin movimiento, hecho con la **M5Stack CoreS3 Lite**: escucha, responde con voz, muestra un rostro y el texto en la pantalla, y ve por la cámara. La placa ya viene lista para usar, sin soldaduras.

Dos opciones de «cerebro»:

- **Opción B (predeterminada): servidor local** en esta máquina. Whisper → `claude -p` con la suscripción → Chatterbox. Sin costo por pregunta (usa la suscripción de Claude).
- **Opción A: conexión directa a una API** de voz en tiempo real (Gemini Live u OpenAI Realtime). Solo está diseñada: no se llama a nada sin la autorización de Nei (Nei Maldaner, autor del proyecto).

**Estado al 15/11/2026: servidor de la opción B listo (F1), la placa todavía no ha llegado.** Con la respuesta por partes, el primer sonido sale en 6,8 a 7,6 s, y una frase de espera («déjame ver la hora…») cubre el silencio; 19 s en la primera respuesta después de 10 min sin actividad; la foto también funciona. El firmware es un esqueleto que compila y muestra la PSRAM.

| Para | Dónde |
|---|---|
| Entender qué es y qué se decidió | [DEFINICAO.md](DEFINICAO.md) (en portugués) |
| Comprar | [LISTA-DE-COMPRAS.md](LISTA-DE-COMPRAS.md) (en portugués) |
| Fases y criterios para dar cada una por terminada | [PLANO.md](PLANO.md) (en portugués) |
| Servidor local (opción B) | [servidor/README.md](servidor/README.md) |
| Programa de la placa | [firmware/README.md](firmware/README.md) |
| Preguntas y límites (API, placas, cámara, movimiento) | [FAQ.md](FAQ.md) (en portugués) |
| Versión anterior (XIAO soldada en un cubo de 40 mm) | [arquivo/variante-xiao/](arquivo/variante-xiao/DEFINICAO.md) (en portugués) |
| Retomar el trabajo | [handoffs/latest.md](handoffs/latest.md) (en portugués) |

## En números

- Placa: 54 × 54 × 16,5 mm, 54 g. Pantalla de 2", 320 × 240, táctil. Cámara de 0,3 MP. Batería de 200 mAh.
- Precio: R$ 256,55 en la tienda oficial de M5Stack en AliExpress (consultado el 15/11/2026, sin envío ni impuestos).
- Audio: 16 kHz, 16 bits, mono, en ambos sentidos. Habla de hasta 15 s.
- Opción B, medido el 15/11: primer sonido en 6,8 a 7,6 s con la respuesta por partes (caliente), 19 s desde que se toca en el caso frío. Detalles en [servidor/MEDIDAS.md](servidor/MEDIDAS.md) (en portugués).

## El proceso, de principio a fin

Leyenda: 🧠 sesión con Nei · ⚙️ comando/script · 🤖 `claude -p`

| # | Paso | Comando | Quién | ¿Existe hoy? |
|---|---|---|---|---|
| 1 | Leer la definición y elegir voz y opción | [DEFINICAO.md](DEFINICAO.md) (en portugués), sección 3 | 🧠 | sí |
| 2 | Comprar la CoreS3 Lite | [LISTA-DE-COMPRAS.md](LISTA-DE-COMPRAS.md) (en portugués) | 🧠 | sí |
| 3 | Copiar el `.env` del servidor y elegir el token | `cp servidor/env.exemplo servidor/.env` | 🧠 | sí |
| 4 | Iniciar el servidor (opción B); inicia Whisper y la voz residente | `python3 servidor/servidor.py` | ⚙️ | sí |
| 5 | Probar el servidor sin el robot, con foto y sin ella | `python3 servidor/testar.py servidor/teste/pergunta.wav` (y `--foto`, `--limites`) | ⚙️ | sí |
| 5b | Grabar las frases de espera con la voz del robot (solo una vez o al cambiar la voz) | `python3 servidor/gerar_espera.py` | ⚙️ | sí (32 frases) |
| 6 | En cada turno: escribir la respuesta | `claude -p --model haiku --tools "" --strict-mcp-config --no-session-persistence …` | 🤖 | comando probado |
| 7 | Instalar las bibliotecas de la placa (avisarle a Nei) | `arduino-cli lib install M5Unified M5GFX` | ⚙️ | no: fase F2 |
| 8 | Completar el Wi-Fi, el servidor, el token y el cerebro | `cp firmware/robo_fala/segredos.exemplo.h firmware/robo_fala/segredos.h` | 🧠 | sí |
| 9 | Compilar el firmware | `arduino-cli compile --fqbn esp32:esp32:m5stack_cores3 firmware/robo_fala` | ⚙️ | sí (esqueleto) |
| 10 | Grabarlo en la placa | `arduino-cli upload --fqbn esp32:esp32:m5stack_cores3 -p /dev/ttyACM0 firmware/robo_fala` | ⚙️ | no probado: sin placa |
| 11 | Conversar en la mesa de trabajo: 5 preguntas seguidas | [PLANO.md](PLANO.md) (en portugués), fase F2 | 🧠 | — |
| 12 | Opción A, conexión directa a la API | solo con autorización de Nei: [PLANO.md](PLANO.md) (en portugués), fase F3 | 🧠 | — |
| 13 | Visión: foto y algunos cuadros | [PLANO.md](PLANO.md) (en portugués), fase F4 | 🧠 | — |
| 14 | Guía PT/EN/ES en `guia/` (skill `projetos-landing-guia`, traducción mediante `inema-traduz`, revisor independiente) | `guia/index.html`, `guia/en/`, `guia/es/` | 🧠 + 🤖 | sí (15/11/2026) |
| 15 | Publicar: push a `main`; GitHub Pages se publica mediante Actions | `git push` → https://inematds.github.io/robo-cores3-lite/guia/ | ⚙️ | sí |
| 16 | Portal inema.club, inemabuscas y catálogo PRO | skill `atualiza-portal` | 🧠 | sí — [PUBLICACAO.md](PUBLICACAO.md) (en portugués) |
| 17 | Tema en el grupo INEMA.ROBOT de Telegram + MENU | skill `postar-telegram` | 🧠 | sí — [PUBLICACAO.md](PUBLICACAO.md) (en portugués) |
| 18 | Video en el canal lives6 y en la guía | otro agente; marca `<!-- VIDEO: -->` en la guía | 🧠 | sí (15/11/2026) — [lives6](https://www.youtube.com/watch?v=ckhcNbClXNs) |

En el robot, el único paso con `claude -p` es el 6, con la suscripción y sin herramientas. El 🤖 del paso 14 corresponde a la traducción y al revisor.

## Reglas

- Ninguna API externa sin autorización explícita de Nei (servicio y finalidad). La opción A existe solo en el papel.
- Claude solo con la suscripción (`claude -p`), nunca con una clave de API.
- Repositorio público en https://github.com/inematds/robo-cores3-lite (publicado por orden de Nei el 15/11/2026).