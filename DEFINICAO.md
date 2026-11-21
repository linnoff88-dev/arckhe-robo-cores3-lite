# DEFINICAO — robo-cores3-lite

Reescrita em 15/11/2026, quando o projeto trocou de placa. Nada foi comprado nem gravado numa placa ainda.
A versão anterior (XIAO ESP32S3 soldada num cubo impresso de 40 mm) está guardada em
[arquivo/variante-xiao/](arquivo/variante-xiao/DEFINICAO.md).

## 1. Objetivo

Um robô de mesa quadrado, sem movimento, que conversa com você por voz, mostra um rosto e o texto na tela e
enxerga pela câmera. A placa é a **M5Stack CoreS3 Lite**, que já vem pronta: tela, câmera, microfones, falante,
bateria e caixa num quadrado de 54 mm. Nada de solda.

Pedidos do Nei, literais:
- 14/11/2026: "quero fazer uma solução simples usando ESP32 e ele apenas falando comigo através de uma API, um robô
  o menor possível, quadrado, sem movimentação".
- 15/11/2026: "quero duas opções, uma solução falar direto com uma api, e a outra falar com um servidor. quero tela,
  mic e voz, uma opção a mais seria reconhecer imagem e vídeo".
- 15/11/2026: "foca na lite e segue, então já muda o nome do projeto para focar nesta aqui".

## 2. O que o robô faz e o que não faz

| Faz | Não faz |
|---|---|
| Grava a sua fala enquanto você segura o dedo na tela (até 15 s) | Não anda, não gira: sem motor |
| Manda a gravação para o "cérebro": servidor local (opção B) ou API na nuvem (opção A) | Não entende a fala sozinho: sem servidor ou API, fica mudo |
| Toca a resposta em voz e mostra o texto na tela | Não escuta e fala ao mesmo tempo: microfone e falante dividem o mesmo barramento (seção 6) |
| Mostra um rosto com o estado: ouvindo, pensando, falando, erro | Não escuta o tempo todo na primeira versão: só com o dedo na tela |
| Tira uma foto quando você pede e manda junto com a pergunta | Não manda vídeo de verdade: no máximo uns poucos quadros por segundo, em 640 × 480 |
| Funciona no cabo USB-C; a bateria de 200 mAh segura uns minutos fora dele (não medido) | Não lê texto pequeno pela câmera (0,3 MP) |

## 3. Decisões tomadas e o que fica com o Nei

| Assunto | Escolha | Por quê |
|---|---|---|
| Placa | M5Stack CoreS3 Lite | Única das três vistas que tem câmera, sem solda e a mais barata com câmera; seção 5 |
| Foco | Só a CoreS3 Lite | Pedido do Nei em 15/11. A Waveshare 1,54" fica como variante futura só de voz; seção 5 |
| Ativação | Segurar o dedo na tela para falar | A Lite não tem botão livre para o usuário (só liga/desliga e reinicia) |
| Cérebro, opção B | Servidor local: Whisper → `claude -p` → Chatterbox | Custo zero; regra: Claude só pela assinatura; seção 9 |
| Cérebro, opção A | Direto numa API de voz em tempo real | Pedido do Nei. **Só desenho: nada é chamado sem autorização**; seção 10 |
| Ordem | B primeiro, A depois | B não precisa de autorização nem de placa para começar (F1) |
| Voz da opção B | Chatterbox local, voz `rachel` | Voz padrão da regra global; troca em uma linha do `.env` |
| Firmware | Arduino pelo `arduino-cli`, core `esp32:esp32` 3.3.12, placa `m5stack_cores3` | Já instalado; a placa CoreS3 já existe no core |
| Energia | USB-C, no cabo | Robô de mesa |

Fica com o Nei:
1. Comprar a CoreS3 Lite ([LISTA-DE-COMPRAS.md](LISTA-DE-COMPRAS.md)) e dizer o preço em reais que aparece.
2. Confirmar a voz `rachel` ou escolher outra.
3. Para a opção A: dizer qual API avaliar (Gemini Live, OpenAI Realtime ou as duas) e autorizar por escrito o uso
   e a finalidade. Sem isso a opção A não sai do papel.
4. Para a opção A: dizer se o robô precisa funcionar longe de casa (vai direto na API) ou se pode passar pelo
   servidor (seção 10, variante A2).

## 4. Arquitetura

```
                        ┌───────────── opção B (padrão) ─────────────┐
 CoreS3 Lite ──Wi-Fi──▶ │ servidor local, porta 8770, máquina do Nei │
 tela + câmera          │  Whisper (inemavox) → claude -p → Chatterbox│
 mic + falante          └────────────────────────────────────────────┘
        │
        └──Wi-Fi──▶ opção A: API de voz em tempo real (Gemini Live ou OpenAI Realtime)
                    só com autorização do Nei; nenhuma chamada implementada
```

O firmware tem uma camada de "cérebro" com as duas implementações, escolhida em `segredos.h`. Tela, microfone,
falante e câmera ficam numa camada de hardware separada, para a Waveshare poder entrar depois trocando só ela.

## 5. A placa: CoreS3 Lite

Especificações lidas na matéria da CNX Software de 22/07/2025 (seção 13), não na página do fabricante:

| Item | CoreS3 Lite |
|---|---|
| Processador | ESP32-S3 (ESP32-S3FN16R8), dois núcleos, 240 MHz, Wi-Fi 2,4 GHz e Bluetooth 5 |
| Memória | 16 MB de flash, 8 MB de PSRAM |
| Tela | 2", 320 × 240, IPS, com toque capacitivo |
| Câmera | GC0308, 0,3 MP (640 × 480), até 30 quadros por segundo |
| Som | Falante de 1 W com amplificador AW88298; dois microfones no conversor ES7210 |
| Sensores | Proximidade (LTR-553), movimento de 6 eixos (BMI270), bússola (BMM150), relógio (BM8563) |
| Energia | USB-C 5 V, bateria interna de 200 mAh, controlador AXP2101 |
| Expansão | Uma porta Grove I²C, microSD |
| Tamanho e peso | 54 × 54 × 16,5 mm, 54 g; traseira magnética |
| Preço | US$ 44,90 de tabela em jul/2025 (CNX). R$ 256,55 na loja oficial do AliExpress, lido em 15/11/2026, sem frete nem imposto |

Comparação com as outras placas vistas em 15/11/2026:

| Placa | Câmera | Tela | Mic + falante | Bateria | Preço de tabela |
|---|---|---|---|---|---|
| **M5Stack CoreS3 Lite** | ✅ | 2", toque | ✅ | 200 mAh | US$ 44,90 |
| M5Stack CoreS3 (completa) | ✅ | 2", toque | ✅ | 500 mAh + base DIN | US$ 59,90 |
| M5Stack CoreS3 SE | ❌ | 2", toque | ✅ | não tem | US$ 38,90 |
| Waveshare ESP32-S3-(Touch-)LCD-1.54 | ❌ | 1,54", 240 × 240 | ✅ | conforme a versão | não lido |

- A **base DIN** da CoreS3 completa serve para prender a placa em trilho de painel elétrico e ligar em 9–24 V.
  O robô não precisa dela. Por isso a Lite.
- A **Waveshare** fica como variante futura, menor e só de voz: o chip da tela (ST7789) e o do som
  (ES8311 + NS4150B) são outros, então ela entra trocando a camada de hardware do firmware.

## 6. Som: microfone e falante não funcionam ao mesmo tempo

Na CoreS3, o conversor dos microfones (ES7210) e o amplificador do falante (AW88298) usam o mesmo barramento I²S.
A documentação da M5Stack diz que os dois não podem ser usados ao mesmo tempo, e o exemplo dela desliga um
(`M5.Mic.end()`) antes de ligar o outro (`M5.Speaker.begin()`). Exemplos da comunidade esperam de 200 a 500 ms na
troca. Fontes na seção 13.

O que isso muda:
- A conversa é **meio a meio**: ou o robô ouve, ou fala.
- **Interromper a fala do robô é pelo toque na tela, não pela voz.** O toque para o falante e liga o microfone.
- Na opção A, o "pode interromper" das APIs em tempo real só vale pelo toque. A escuta contínua com interrupção
  por voz precisaria de microfone externo (porta Grove) ou de outra placa. Não está no plano.

## 7. Tela e toque

- O rosto ocupa a tela: olhos que piscam, mudam com o estado (ouvindo, pensando, falando, erro, sem Wi-Fi).
- Embaixo, uma faixa com o texto da resposta, como legenda.
- **Segurar o dedo na tela = falar.** Soltar = enviar. Toque rápido durante a fala do robô = parar.
- Toque duplo = tirar foto e perguntar "o que você está vendo?" (a definir na F4).

## 8. Câmera

- A câmera vai pelo `esp_camera`, que já vem no core instalado (`espressif__esp32-camera`, conferido em 15/11/2026).
  A biblioteca M5Unified cuida da tela, do toque, do som e da energia, **não da câmera**.
- **Foto na hora:** quadro JPEG de 640 × 480 tirado quando você começa a falar, se a pergunta pedir visão
  (ou sempre, a decidir na F4 medindo o tempo a mais).
- **"Vídeo":** sequência de poucos quadros por segundo. Na opção A com Gemini Live, os quadros entram na mesma
  conexão do áudio. Na opção B, cada pergunta leva no máximo umas poucas fotos.
- Pinos da câmera: documentação da M5Stack para a CoreS3 (seção 13). Conferir na F4 com a placa na mão.

## 9. Opção B: servidor local (padrão)

1. Você segura o dedo na tela. O robô grava para a PSRAM (16 kHz, 16 bits, mono).
2. Se for pergunta com visão, ele manda a foto antes (`POST /v1/foto`).
3. Você solta. O robô manda o WAV (`POST /v1/fala`).
4. O servidor transcreve (Whisper do inemavox), pede a resposta ao `claude -p` pela assinatura e gera a voz
   (Chatterbox do inemavox).
5. O robô recebe o WAV, troca o barramento para o falante, toca e mostra o texto.

| Etapa | Como | Conferido |
|---|---|---|
| Transcrição | inemavox `127.0.0.1:8010`: `POST /api/jobs/transcribe/upload`; ou o Whisper residente na porta 7871 | API respondeu `ok` (v1.15.4) em 14/11; nenhuma transcrição feita |
| Resposta | `claude -p --model haiku --tools "" --strict-mcp-config --no-session-persistence`, pasta vazia, `env -u ANTHROPIC_API_KEY` | **Respondeu em 5,0 s em 14/11** |
| Resposta com foto | Como a imagem entra no `claude -p` sem liberar ferramentas **não foi testado**. Candidato: entrada `--input-format stream-json` com um bloco de imagem. A F1 prova; a trava "sem ferramentas" não se afrouxa sem o Nei | não testado |
| Voz | inemavox `POST /api/jobs/tts/upload` (força o Chatterbox local) | rotas lidas; nenhuma voz gerada |
| Conversão | `ffmpeg` para WAV 16 kHz mono 16 bits | instalado |

Travas: a rota `/api/jobs/tts` sem `engine` e o `chatterbox-vc` usam o Edge, que é serviço online: proibidos.
`claude -p` nunca com `--bare`. O texto que chega ao Claude é fala de qualquer pessoa perto do robô: sempre sem
ferramentas, sem MCP, sem sessão salva. Detalhe em [servidor/README.md](servidor/README.md).

## 10. Opção A: direto numa API (só desenho, nada implementado)

**Nenhuma chamada a API externa acontece sem autorização explícita do Nei, por escrito, dizendo o serviço e a
finalidade.** Ter chave em `.env` não é autorização. A API da Anthropic não é opção: Claude só pela assinatura.

| Candidata | O que faz | Visão | Observação |
|---|---|---|---|
| Gemini Live (Google) | Áudio entra e sai em tempo real por WebSocket | Recebe quadros da câmera na mesma conexão | A mais indicada para "fica olhando e me diz" |
| OpenAI Realtime | Áudio entra e sai em tempo real por WebSocket | Recebe imagem | Pago por uso |

Duas variantes, a escolher pelo Nei:

| Variante | Caminho | A favor | Contra |
|---|---|---|---|
| A1, direto | Robô → API | Funciona em qualquer Wi-Fi, longe de casa | A chave da API fica gravada no robô; WebSocket com áudio contínuo no firmware |
| A2, via servidor | Robô → servidor → API | A chave fica no PC; o firmware é o mesmo da opção B | Depende do PC ligado, como a B |

Demora esperada da opção A: perto de 1 s, contra os 8 a 20 s estimados da B. É estimativa, não medida.

## 11. Protocolo robô ↔ servidor (opção B)

HTTP, um pedido e uma resposta por turno. Porta 8770 (a 8765 está ocupada nesta máquina, conferido em 14/11).

**Foto (opcional, antes da fala)**

```
POST /v1/foto
Content-Type: image/jpeg
X-Robo-Token: <token>
X-Robo-Id: lite-1

<JPEG 640 × 480, até 200 kB>
```

Resposta `200 {"turno": "<id>"}`. O servidor guarda a foto por 60 s.

**Fala**

```
POST /v1/fala
Content-Type: audio/wav
X-Robo-Token: <token>
X-Robo-Id: lite-1
X-Turno: <id da foto, se houve>

<WAV PCM, 16 000 Hz, 16 bits, mono, de 0,5 a 15 s>
```

| Código | Corpo | O robô faz |
|---|---|---|
| 200 | WAV PCM 16 kHz mono 16 bits | Toca e mostra o texto de `X-Resposta` |
| 204 | Vazio: curto (< 0,5 s), silencioso (volume médio < −50 dB, medido antes do Whisper) ou sem texto | Rosto de "não entendi" e volta a pronto |
| 401 | `{"erro": "token"}` | Rosto de erro |
| 413 | `{"erro": "grande"}` (fala > 1 MB, foto > 200 kB) | Rosto de erro |
| 415 | `{"erro": "formato"}` | Rosto de erro |
| 500 / 503 | `{"erro": "<etapa>"}` | Rosto de erro e volta a pronto sem reiniciar |

Cabeçalhos da resposta 200 (UTF-8 com codificação de URL, até 500 caracteres): `X-Ouvido`, `X-Resposta` e
`X-Tempos` (`stt=1.2;llm=5.0;tts=8.0;total=14.6`, em segundos).

**Conversa por partes (rota principal do robô, desde 15/11/2026):** `POST /v1/conversa`, mesmo pedido da `/v1/fala`.
As recusas (401, 204, 413, 415) vêm antes, iguais. Depois do 200, o corpo é uma sequência de quadros, cada um com
1 byte de tipo, 4 bytes de tamanho (little-endian) e os dados, enviados assim que cada etapa termina:

| Tipo | Dados | Chega (medido, quente) | O robô faz |
|---|---|---|---|
| `E` | id de uma frase de espera (ex.: `hora-02`) | logo depois do `O` (ou antes, no caso frio) | Toca a frase guardada na memória dele |
| `O` | o que o servidor ouviu (texto) | ~0,5 s | Mostra "Você disse: …" e o rosto de "entendi" |
| `T` | texto de uma parte da resposta | 6,8–8,5 s a 1ª | Mostra como legenda |
| `A` | WAV 16 kHz mono 16 bits dessa parte | junto com o `T` | Toca; as partes seguintes chegam enquanto toca |
| `F` | JSON com a resposta inteira e os tempos | no fim | Volta a pronto |
| `X` | JSON com o erro | se algo falhar no meio | Rosto de erro |

**Aquecer:** `POST /v1/aquecer` (com o token, sem corpo) → `202 {"frio": true|false}`. O robô chama quando o dedo
encosta na tela: se os modelos estiverem descarregados, eles sobem enquanto a pessoa fala.

**Frases de espera:** `GET /v1/espera` → lista (id, categoria, texto, segundos); `GET /v1/espera/<id>.wav` → o áudio.
O robô baixa a banca uma vez (32 frases, 3,1 MB) e toca da memória dele. Regras de escolha em `servidor/espera.py`:
categoria pelo que a pessoa disse (hora, foto, conta, pergunta difícil, geral; saudação curta não ganha frase), nunca
repete uma das últimas 8, pula 1 vez em 3 (nunca no caso frio).

**Saúde:** `GET /saude` → `{"ok": true}`. **Limites:** fala de até 15 s (480 044 bytes); o robô espera até 90 s.

**Estados:** `PRONTO` → (dedo na tela) `OUVINDO` → (soltou) `PENSANDO` → `FALANDO` → `PRONTO`.
Falha: `ERRO` por 2 s e volta a `PRONTO`. Toque durante `FALANDO` → `PRONTO`.

## 12. Firmware

- `arduino-cli`, core `esp32:esp32` 3.3.12, FQBN `esp32:esp32:m5stack_cores3`.
- A placa `m5stack_cores3` do core tem PSRAM ligada por padrão no modo QSPI (`PSRAM=enabled`, lido no `boards.txt`
  em 15/11). **Não verificado:** se essa definição de placa vale para a Lite sem ajuste. O esqueleto mostra o
  tamanho da PSRAM pela serial; se vier 0, testar `PSRAM=opi`.
- Bibliotecas a instalar na F2: `M5Unified` e `M5GFX` (`arduino-cli lib install M5Unified M5GFX`). É um download
  novo: avisar o Nei antes. A câmera usa o `esp_camera` do core; som pelo `M5.Mic` e `M5.Speaker`.

## 13. Fontes lidas em 15/11/2026

- CoreS3 Lite, especificações e preços de tabela (Lite, CoreS3, SE): https://www.cnx-software.com/2025/07/22/m5stack-cores3-lite-low-cost-iot-controller-features-magnetic-backplate-and-200mah-battery/
- CoreS3, documentação oficial: https://docs.m5stack.com/en/core/CoreS3
- CoreS3 a US$ 59,90 com câmera VGA: https://www.cnx-software.com/2023/05/05/60-m5stack-cores3-esp32-s3-iot-controller-comes-with-2-inch-display-vga-camera-multiple-sensors/
- Microfone e falante não ao mesmo tempo (M5Stack): https://docs.m5stack.com/en/arduino/m5cores3/mic
- Barramento I²S dividido, troca de 200–500 ms (comunidade): https://lilting.ch/en/articles/m5stack-cores3-voice-chat-spec-check
- Anúncios da loja oficial M5Stack no AliExpress (título lido, preço não):
  CoreS3 Lite https://pt.aliexpress.com/item/1005009527295120.html ·
  CoreS3 completa https://pt.aliexpress.com/item/1005005495395891.html ·
  CoreS3 SE https://pt.aliexpress.com/item/1005007059753733.html
- Waveshare ESP32-S3-LCD-1.54 (fotos e lista de componentes do anúncio): https://pt.aliexpress.com/item/1005012716829974.html
- Placa no core: `arduino-cli board details -b esp32:esp32:m5stack_cores3` e `boards.txt` do core 3.3.12
- inemavox: `~/projetos/inemavox/CLAUDE.md`, `api/server.py`, `api/job_manager.py`; `claude --help`

## 14. O que ainda não foi verificado

- Nada foi comprado. O preço em reais não foi lido (o AliExpress só mostra no navegador).
- As especificações da Lite vêm da CNX Software, não da página oficial.
- A definição de placa `m5stack_cores3` na Lite e o modo da PSRAM.
- Nenhuma transcrição nem voz foi gerada para o projeto. Só o `claude -p` foi medido: 5,0 s, uma vez.
- Como mandar uma foto ao `claude -p` sem liberar ferramentas.
- A troca do barramento entre microfone e falante na prática (tempo e estalo).
- A opção A inteira: nenhuma API foi chamada.
