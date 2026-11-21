# DEFINICAO — robô ESP32 que só fala

> **Arquivado em 15/11/2026.** O projeto trocou para a placa pronta M5Stack CoreS3 Lite (ver `../../DEFINICAO.md`).
> Este arquivo descreve a variante antiga, XIAO ESP32S3 soldada num cubo impresso de 40 mm. Só referência.

Escrita em 14/11/2026. Nada foi comprado, soldado, impresso nem programado. Este arquivo é o ponto de partida.

## 1. Objetivo

Um cubo de mesa, o menor possível, com um ESP32 dentro. Você aperta o botão, fala, e ele responde com voz.
O ESP32 só grava e toca: quem entende, pensa e gera a voz é um servidor local na sua máquina, sem API externa.
Sem motor, sem servo, sem rodas.

Pedido do Nei, literal: "quero fazer uma solução simples usando ESP32 e ele apenas falando comigo através de uma
API, um robô o menor possível, quadrado, sem movimentação".

## 2. O que o robô faz e o que não faz

| Faz | Não faz |
|---|---|
| Grava a sua fala enquanto o botão está apertado (até 15 s) | Não anda, não gira, não inclina: sem motor, sem servo, sem rodas |
| Manda a gravação por Wi-Fi para o servidor local | Não entende a fala sozinho: sem servidor ligado, ele não responde |
| Toca a resposta em voz pelo falante | Não escuta o tempo todo (fase 1): só com o botão apertado |
| Mostra o estado por um LED (pronto, gravando, pensando, falando, erro) | Não tem câmera, não tem tela (tela pequena fica como opcional) |
| Liga pelo cabo USB-C | Não usa bateria na fase 1 |
| | Não chama nenhuma API de nuvem |

## 3. Decisões já tomadas (padrão) e o que fica com o Nei

| Assunto | Escolha | Por quê |
|---|---|---|
| Placa | Seeed Studio XIAO ESP32S3 (sem "Sense") | 21 × 17,8 mm, 8 MB de PSRAM, carregador de bateria na placa; seção 5 |
| Microfone | INMP441 (I²S), em módulo | Fica onde a caixa precisar, longe do falante |
| Som | MAX98357A (I²S) + falante de 28 mm, 8 Ω | Um módulo só faz o papel de DAC e amplificador |
| Ativação | Botão: aperta e segura para falar | Sem modelo de palavra de ativação, sem escuta contínua |
| Energia | USB-C, sempre no cabo | O robô não sai da mesa; seção 8 |
| Servidor | Local, na máquina do Nei | Regra: nenhuma API externa sem autorização |
| Transcrição | Whisper local do inemavox | Já aprovado |
| Resposta | `claude -p` pela assinatura, sem ferramentas | Regra: Claude só pela assinatura |
| Voz | Chatterbox local do inemavox, voz `rachel` | É a voz padrão da regra global; troca em uma linha do `.env` |
| Protocolo | HTTP POST de um WAV, resposta em WAV | Um pedido, uma resposta; dá para testar com um comando; seção 11 |
| Firmware | Arduino (core esp32 3.3.12) pelo `arduino-cli` | Já está instalado na máquina; nada a instalar |
| Tamanho | Cubo de 40 mm de lado (mínimo calculado: 37,0 mm) | Seção 12 |

Fica com o Nei:
1. Comprar as peças ([LISTA-DE-COMPRAS.md](LISTA-DE-COMPRAS.md)).
2. Confirmar ou trocar a voz (`rachel`, `nei`, `nei2`, `nei3`, `nei4`, `bella`).
3. Dizer se prefere o atalho pronto (M5Stack Atom Echo, seção 5), que dispensa solda e caixa.
4. Autorizar, se quiser, alguma opção de nuvem da seção 10. Nenhuma está implementada.

## 4. Arquitetura em blocos

```
            ROBÔ (cubo de 40 mm)                              SERVIDOR LOCAL (máquina do Nei)
 ┌──────────────────────────────────────┐            ┌──────────────────────────────────────────────┐
 │ botão ─────────┐                     │            │ servidor/servidor.py  (porta 8770)           │
 │ microfone I²S ─┤                     │   Wi-Fi    │   1. recebe o WAV                            │
 │   (INMP441)    ├─ XIAO ESP32S3 ──────┼──HTTP──────┼─► 2. Whisper local (inemavox)   fala → texto │
 │ amplificador ◄─┤   8 MB PSRAM        │   POST     │   3. claude -p (assinatura)      texto → texto│
 │   (MAX98357A)  │                     │◄───WAV─────┼── 4. Chatterbox local (inemavox) texto → voz │
 │      │         │                     │            │   5. ffmpeg: WAV 16 kHz mono 16 bits         │
 │   falante 28 mm│   USB-C 5 V ◄── fonte            │                                              │
 └──────────────────────────────────────┘            └──────────────────────────────────────────────┘
```

| Bloco | Peça | Papel |
|---|---|---|
| Cérebro do robô | XIAO ESP32S3 | Lê o botão, grava do microfone para a PSRAM, envia, toca a resposta |
| Ouvido | INMP441, I²S | Microfone digital. Sai áudio já em números, sem ruído de fio analógico |
| Boca | MAX98357A, I²S + falante 28 mm | Recebe áudio digital e move o falante |
| Ativação | Chave táctil 6 × 6 mm | Aperta e segura para falar |
| Estado | LED da própria placa (GPIO21) na bancada; "olhos" opcionais depois | Mostra o que o robô está fazendo |
| Energia | USB-C da própria placa | 5 V do cabo |
| Servidor | Python na máquina do Nei | Transcreve, responde, sintetiza |

## 5. Placa: recomendada e alternativas

Recomendada: **Seeed Studio XIAO ESP32S3 (sem "Sense")**.

| Placa | Medidas | Memória | Áudio na placa | Bateria | Fonte |
|---|---|---|---|---|---|
| **XIAO ESP32S3** (recomendada) | 21 × 17,8 mm | 8 MB PSRAM + 8 MB flash | Nenhum: microfone e amplificador por fora | Chip de carga na placa | P: wiki da Seeed |
| XIAO ESP32S3 Sense | 21 × 17,8 × 15 mm com a placa de expansão | 8 MB PSRAM + 8 MB flash + cartão SD | Microfone digital PDM (relógio GPIO42, dado GPIO41) e câmera | Chip de carga na placa | P: wiki da Seeed |
| M5Stack Atom Echo ("Atom Voice" na documentação atual) | 24,0 × 24,0 × 16,8 mm, 9 g, já com caixa | ESP32-PICO-D4, 4 MB flash; a ficha não lista PSRAM | Microfone SPM1423 (PDM), amplificador NS4168, falante de 0,8 W, botão e LED RGB | Não tem | P: docs.m5stack.com |
| M5Stack Atom EchoS3R | 24,0 × 24,0 × 16,8 mm (NC: medida de loja) | ESP32-S3 com 8 MB PSRAM + 8 MB flash (T) | Codec ES8311, microfone MEMS, amplificador NS4150B, falante 8 Ω 1 W (T) | Não lido | T: openelab.io e mouser.com |
| ESP32-S3-BOX-3 | Corpo não lido. Só a tela de 2,4" tem 61 mm de diagonal | 16 MB PSRAM + 16 MB flash | 2 microfones, falante, tela de toque | Não lido | T: cnx-software.com |
| Waveshare ESP32-S3-Zero | NC (a página só mostra a medida em imagem) | 2 MB PSRAM + 4 MB flash | Nenhum | Não tem carregador | P: wiki da Waveshare |

Por que a XIAO ESP32S3:
- **PSRAM de 8 MB.** 15 s de fala a 16 kHz, 16 bits, mono ocupam 480 kB. Na PSRAM isso cabe inteiro, e o firmware
  fica direto: grava tudo, depois envia. Sem PSRAM seria preciso enviar enquanto grava.
- **21 × 17,8 mm.** É a menor placa da tabela com PSRAM e medida confirmada.
- **Carregador de LiPo na placa.** A bateria, se um dia entrar, são 2 pontos de solda.
- **A placa já está no `arduino-cli` desta máquina** (`esp32:esp32:XIAO_ESP32S3`, core 3.3.12).

Por que não as outras:
- **Sense:** tira um componente (o microfone já vem), mas o microfone fica preso à posição da placa, que por sua vez
  fica presa ao USB-C na parede de trás. Com o INMP441 separado, o furo do microfone vai para a frente, longe do
  falante. A Sense fica como plano B se a solda do INMP441 der trabalho: o firmware muda só o modo do microfone
  (PDM em vez de I²S padrão).
- **Atom Echo: é o menor de todos e já vem pronto.** Um cubo de 24 mm com microfone, falante, botão e LED, sem solda.
  Se o que importa é só o menor tamanho, é ele. Ficou como alternativa por três motivos: não tem PSRAM na ficha
  (o envio teria de ser feito enquanto grava), o falante é de 0,8 W, e a compra no Brasil não foi conferida.
  O Atom EchoS3R resolve a memória, mas as medidas e a disponibilidade vêm só de loja. **Decisão do Nei.**
- **ESP32-S3-BOX-3:** a tela sozinha já é maior que o cubo inteiro.
- **ESP32-S3-Zero:** serve e costuma ser mais barata, mas tem 2 MB de PSRAM, não tem carregador e a medida não foi lida.

Cuidados com a XIAO, lidos na wiki da Seeed:
- A antena é externa, num conector U.FL. Sem a antena ligada o Wi-Fi fica fraco. Ela precisa de lugar na caixa.
- Na bateria, o pino 5V não tem tensão. Isso muda a alimentação do amplificador (seção 8).
- A placa não tem pino para ler a tensão da bateria.

## 6. Som: microfone, amplificador, falante

| Peça | Medidas | Fonte | Observação |
|---|---|---|---|
| INMP441 (módulo redondo) | Ø 14 mm, 3,5 mm de espessura com solda | NC | Conferir de que lado da placa fica o furo do som antes de desenhar o furo da caixa |
| MAX98357A (módulo) | 19,4 × 17,8 × 3,0 mm, 1,2 g | P: Adafruit 3006. Módulo genérico: NC | 2,7 a 5,5 V. Ganho de fábrica 9 dB. 3,2 W em 4 Ω a 5 V (com 10% de distorção) |
| Falante 28 mm, 8 Ω, 2 W | Ø 28 mm (T), altura 10 mm (NC) | Anúncio | Com 8 Ω a potência fica abaixo dos 3,2 W: sobra para voz em mesa |
| Falante 40 mm, 4 Ω, 3 W (opção) | Ø 40 mm (T), altura 20 mm (NC) | Anúncio | Voz mais cheia. O cubo sobe para 50 mm |

- Áudio nos dois sentidos: 16 kHz, 16 bits, mono. Para voz, basta, e um falante de 28 mm não reproduz muito além disso.
- O robô nunca grava e toca ao mesmo tempo. Enquanto fala, o microfone fica desligado. Isso evita eco sem precisar
  de cancelamento.

## 7. Ativação e "olhos"

- **Fase 1: botão.** Aperta e segura: grava. Solta: envia. Um aperto durante a fala interrompe a resposta.
- **Palavra de ativação: depois, se o Nei quiser.** O core instalado traz a biblioteca `ESP_SR` (não testada aqui).
  Não foi verificado se existe palavra em português. Entra como decisão, não como tarefa.
- **Olhos (opcional, fora da fase 1):** um LED RGB endereçável atrás de uma parede fina na face da frente, ou uma tela
  OLED de 0,96" por I²C. Os pinos D4, D5 e D6 ficam reservados para isso.
- **Cores sugeridas:** casca preta e botão amarelo, as cores da marca (`#0c0c10` e `#FACC15`).

## 8. Energia: USB-C, sempre no cabo

Escolha: **USB-C direto na XIAO, fonte de 5 V e 1 A ou mais.** Sem bateria na fase 1.

Por quê:
1. O robô não sai da mesa e depende do Wi-Fi e do servidor de casa. Bateria não dá liberdade nenhuma aqui.
2. A mesma porta USB-C grava o programa. Nenhuma peça a mais.
3. Na bateria, o pino 5V da XIAO fica sem tensão. O amplificador teria de ser alimentado pela bateria (3,7 V),
   com menos volume. No cabo, ele recebe 5 V.
4. A bateria soma 6,5 mm ao cubo (de 40 para 46 mm) e um item a mais de risco.

Se a bateria entrar depois: LiPo 1S 3,7 V, 250 mAh, modelo 502030, com proteção, soldada nos dois contatos BAT da
XIAO. A placa já carrega a bateria pelo USB-C. Autonomia não calculada: o consumo com Wi-Fi ligado não foi medido.

## 9. Ligações (proposta, conferir na bancada na F2)

Pinos da XIAO lidos na wiki da Seeed. A escolha de qual pino faz o quê é uma proposta.

| Sinal | Pino da XIAO | GPIO | Vai para |
|---|---|---|---|
| Amplificador: relógio de bits | D0 | 1 | MAX98357A `BCLK` |
| Amplificador: canal | D1 | 2 | MAX98357A `LRC` |
| Amplificador: dado | D3 | 4 | MAX98357A `DIN` |
| Amplificador: alimentação | 5V | — | MAX98357A `Vin` |
| Microfone: relógio de bits | D8 | 7 | INMP441 `SCK` |
| Microfone: canal | D9 | 8 | INMP441 `WS` |
| Microfone: dado | D10 | 9 | INMP441 `SD` |
| Microfone: alimentação | 3V3 | — | INMP441 `VDD` |
| Microfone: seleção de canal | GND | — | INMP441 `L/R` (canal esquerdo) |
| Botão | D7 | 44 | Chave táctil, outro lado no GND (resistor interno ligado) |
| Terra | GND | — | `GND` do amplificador, do microfone e do botão |
| Reservado: tela ou sensor I²C | D4, D5 | 5, 6 | — |
| Reservado: LED dos olhos | D6 | 43 | — |
| Livre | D2 | 3 | Evitar: segundo o datasheet da Espressif é pino de configuração na partida (não relido hoje) |

- São 12 fios saindo da XIAO (3 deles no mesmo GND). Fios de 28 ou 30 AWG, cortados em 6 a 8 cm, soldados direto nas placas.
  **Sem barra de pinos:** ela soma mais de 8 mm de altura e o cubo de 40 mm deixa de fechar.
- Microfone e amplificador usam os dois controladores I²S do ESP32-S3, um para cada. Biblioteca: `ESP_I2S`, que
  vem no core instalado (exemplo `Record_to_WAV`).
- Pinos `SD` e `GAIN` do amplificador ficam soltos (ganho de fábrica). NC no módulo genérico.

## 10. Fluxo de voz e servidor

1. Você aperta o botão. O LED muda. O ESP32 grava do microfone para a PSRAM.
2. Você solta. O ESP32 monta um WAV e manda por HTTP POST para o servidor.
3. O servidor transcreve a fala (Whisper local).
4. O servidor pede a resposta ao `claude -p`, com as últimas trocas da conversa.
5. O servidor gera a voz (Chatterbox local) e converte para WAV 16 kHz mono 16 bits.
6. O ESP32 recebe o WAV e toca enquanto ele chega.

### Servidor padrão: local, sem API externa

| Etapa | Como | Conferido em 14/11/2026 |
|---|---|---|
| Transcrição | inemavox, API em `http://127.0.0.1:8010`: `POST /api/jobs/transcribe/upload` (arquivo + `config_json`), acompanhar em `GET /api/jobs/{id}`, texto em `GET /api/jobs/{id}/transcript?format=txt` | A API respondeu `{"status":"ok","version":"1.15.4"}`. Rotas lidas em `~/projetos/inemavox/api/server.py`. Nenhuma transcrição foi feita |
| Transcrição, caminho rápido | `~/projetos/inemavox/whisper_daemon.py`: o modelo fica na memória, porta 7871, `POST /transcrever {"audio": caminho, "lang": "pt"}` | Estava desligado na hora do teste. Não medido |
| Resposta | `claude -p --model haiku --tools "" --strict-mcp-config --no-session-persistence --system-prompt "<persona>" "<fala>"`, em pasta vazia, com `ANTHROPIC_API_KEY` fora do ambiente | **Testado: respondeu em 5,0 s, pela assinatura** |
| Voz | inemavox: `POST /api/jobs/tts/upload` com o WAV de referência da voz e `config_json` com `text` e `lang`; áudio em `GET /api/jobs/{id}/audio` | Rotas lidas. Nenhuma voz foi gerada |
| Conversão | `ffmpeg` para WAV 16 kHz, mono, 16 bits | `ffmpeg` está instalado |

Três travas, lidas no código e no `CLAUDE.md` do inemavox e no `claude --help`:
- **`POST /api/jobs/tts` sem o campo `engine` usa `edge`, que é o serviço online da Microsoft.** É API externa.
  O servidor do robô só usa `/api/jobs/tts/upload`, que força `chatterbox` (local).
- **`chatterbox-vc` também passa pelo Edge.** Não usar.
- **`claude -p` nunca com `--bare`.** Esse modo só aceita chave de API, e a regra é assinatura.

Segurança do servidor:
- Ele escuta na rede de casa. Todo pedido leva um token no cabeçalho (`X-Robo-Token`), o mesmo no firmware e no `.env`.
- O texto que chega ao `claude -p` é fala transcrita, de qualquer pessoa perto do robô. Por isso ele roda sem
  ferramentas (`--tools ""`), sem MCP e sem salvar sessão: só responde texto.

### Opções que exigem autorização explícita do Nei (nenhuma implementada)

| Opção | O que trocaria | Observação |
|---|---|---|
| OpenAI Realtime API | Transcrição, resposta e voz num serviço só, em tempo real | Pago por uso. Pede WebSocket no firmware |
| Groq (Whisper e modelos de texto) | Transcrição e resposta mais rápidas | As chaves ficam em `~/projetos/openpcbotv2/.env`; ter a chave não é autorização |
| ElevenLabs | Voz com os clones do Nei | Gasta créditos. Citada no `CLAUDE.md` do inemavox |
| Edge TTS (Microsoft), pelo inemavox | Voz sem GPU, rápida | É serviço online. Hoje é o padrão do inemavox quando falta o `engine` |
| Serviço de palavra de ativação na nuvem | Escuta contínua | Não avaliado |

A API da Anthropic não é opção: a regra é Claude só pela assinatura.

Não avaliados, só para registro: firmware aberto `xiaozhi-esp32` e o assistente de voz do ESPHome com Home Assistant.

## 11. Protocolo ESP32 ↔ servidor

Escolha: **HTTP POST de um WAV, resposta em WAV.**

Por quê HTTP e não WebSocket: a conversa com botão é em turnos, um pedido e uma resposta. HTTP usa só a biblioteca
`HTTPClient` do core, e o servidor inteiro pode ser testado sem o robô, com um comando. WebSocket só compensa com
áudio contínuo (palavra de ativação, interromper no meio). Fica para uma versão 2, se a escuta contínua entrar.

**Pedido**

```
POST http://<ip-do-servidor>:8770/v1/fala
Content-Type: audio/wav
Content-Length: <bytes>
X-Robo-Token: <token>
X-Robo-Id: cubo-1

<WAV PCM, 16 000 Hz, 16 bits, mono, de 0,5 a 15 s>
```

**Resposta**

| Código | Corpo | O firmware faz |
|---|---|---|
| 200 | WAV PCM 16 000 Hz, 16 bits, mono, com `Content-Length` | Toca enquanto recebe |
| 204 | Vazio: gravação curta demais (menos de 0,5 s), silenciosa (volume médio abaixo de −50 dB, medido antes do Whisper) ou sem texto | Pisca uma vez e volta a "pronto" |
| 401 | `{"erro": "token"}` | LED de erro |
| 413 | `{"erro": "grande"}` (mais de 1 MB) | LED de erro |
| 415 | `{"erro": "formato"}` (não é WAV 16 kHz mono 16 bits) | LED de erro |
| 500 ou 503 | `{"erro": "<etapa que falhou>"}` | LED de erro e volta a "pronto" sem reiniciar |

Cabeçalhos da resposta 200, para depuração (texto em UTF-8 com codificação de URL, até 500 caracteres):
`X-Ouvido` (o que o Whisper entendeu), `X-Resposta` (o texto falado) e `X-Tempos` (`stt=1.2;llm=5.0;tts=8.0;total=14.6`, em segundos).

**Saúde:** `GET /saude` devolve `{"ok": true}`. O firmware chama uma vez ao ligar.

**Limites:** gravação de até 15 s (480 044 bytes). O firmware espera a resposta por até 90 s.

**Estados do firmware:** `PRONTO` → (botão apertado) `GRAVANDO` → (botão solto) `PENSANDO` → `FALANDO` → `PRONTO`.
Qualquer falha leva a `ERRO` por 2 s e volta a `PRONTO`.

**Porta:** 8770. A 8765 já está ocupada nesta máquina (conferido com `ss -ltn` em 14/11/2026).

## 12. Tamanho do cubo

Conta feita por `python3 cad/caixa_minima.py`, com as medidas de `cad/parametros.py`. **É uma estimativa de pré-CAD:**
a F4 confirma com o modelo 3D e com as peças medidas.

Arranjo, de baixo para cima: pés, base com a grade, falante virado para baixo, amplificador deitado, XIAO deitada com o
USB-C na parede de trás, botão sob o topo. O microfone fica em pé, colado por dentro na parede da frente.

**Largura e profundidade (vale a maior exigência), parede de 2,0 mm:**

| Exigência | Conta | mm |
|---|---|---|
| Falante | 28 + 2 × 0,5 de folga + 2 × 1,2 do anel | 31,4 |
| XIAO + microfone na parede da frente | 21 + 3,5 + 3,0 de fios + 2 × 0,5 | 28,5 |
| Placa mais larga + fios dos dois lados | 17,8 + 2 × 3,0 + 2 × 0,5 | 24,8 |
| **Interno** | a maior | **31,4** |
| **Externo** | 31,4 + 2 × 2,0 de parede | **35,4** |

**Altura (soma da pilha):**

| Camada | mm | Fonte da medida |
|---|---|---|
| Pés (o som sai por baixo) | 3,0 | projeto |
| Base | 2,0 | projeto |
| Falante de 28 mm | 10,0 | NC |
| Vão sobre o falante | 1,5 | projeto |
| Amplificador + fios | 3,0 + 3,0 = 6,0 | P (Adafruit) + NC |
| XIAO + fios | 4,5 + 3,0 = 7,5 | NC + NC |
| Botão | 5,0 | NC |
| Topo | 2,0 | projeto |
| **Total** | **37,0** | |

| Variante | Mínimo calculado | Alvo do projeto | O que manda |
|---|---|---|---|
| **A, padrão: USB-C, falante de 28 mm** | **37,0 mm** | **40 mm** | altura |
| B: com bateria 502030 | 43,5 mm | 46 mm | altura |
| C: falante de 40 mm | 47,4 mm | 50 mm | largura |

- **Resposta: cubo de 40 mm de lado.** O alvo é o mínimo mais 2,5 mm de margem, arredondado para cima, porque 4 das
  8 camadas dependem de medida NC.
- Com parede de 2,4 mm os alvos passam a 41, 47 e 51 mm.
- Medidas NC que mudam o resultado: altura do falante, altura da XIAO, altura do botão, espessura do microfone,
  espaço dos fios.
- Fora da conta: a antena da XIAO (cola numa parede interna; tamanho NC) e o rebaixo para o plugue do cabo USB-C.
- Se a montagem à mão não couber em 40 mm depois da peça de teste, o plano B é 45 mm, sem mudar o arranjo.
- PLA do cubo de 40 mm: cerca de 22 g (estimativa por volume, sem fatiador).

## 13. Onde fica cada abertura (cubo de 40 mm, variante A)

Alturas contadas a partir da mesa, tiradas da pilha da seção 12. A posição final sai do CAD.

| Abertura | Face | Posição | Como fica discreta |
|---|---|---|---|
| Grade do falante | De baixo | Rasgos de 1,5 mm dentro de um círculo de Ø 26 mm | Não aparece: o som sai pelo vão de 3 mm dos pés |
| Furo do microfone | Frente | Um furo de Ø 2 mm, centrado, a cerca de 30 mm da mesa | Um ponto só, longe do falante |
| USB-C | Trás | Centrado, a cerca de 25 mm da mesa; abertura de 9,5 × 3,8 mm (NC) com rebaixo de 12,5 × 7 mm (NC) para o plugue | Fica atrás |
| Botão | Topo | No centro; tecla impressa de Ø 8 mm, rente ao topo | Rente, de outra cor |
| Olhos (opcional) | Frente | Duas janelas de parede fina (0,6 mm), acima do furo do microfone | Sem furo: a luz atravessa o plástico |

Peças impressas previstas: `casca` (4 lados + topo, impressa com o topo na mesa, sem suporte), `base` (com grade,
pés e anel do falante), `berco` (segura a XIAO e o amplificador) e `tecla`. Fecho: 4 parafusos M2 × 8 por baixo (NC)
ou encaixe, a decidir na F4.

## 14. Fontes lidas em 14/11/2026

- XIAO ESP32S3 (medidas, memória, pinos, bateria, microfone da Sense): https://wiki.seeedstudio.com/xiao_esp32s3_getting_started/
- Atom Echo / Atom Voice (medidas, chip, microfone, amplificador): https://docs.m5stack.com/en/atom/atomecho
- MAX98357A (medidas do módulo, potência, tensão, ganho): https://www.adafruit.com/product/3006
- Atom EchoS3R (loja, não oficial): https://openelab.io/products/m5stack-atom-echos3r-smart-speaker e https://www.mouser.com/new/m5stack/m5stack-atoms3r-kits/
- ESP32-S3-BOX-3 (tela, memória, microfones): https://www.cnx-software.com/2023/09/01/esp32-s3-box-3-devkit-comes-with-2-4-inch-display-dual-microphone-pcie-expansion-connector/
- ESP32-S3-Zero (memória, 2 controladores I²S): https://www.waveshare.com/wiki/ESP32-S3-Zero
- Rotas e padrões do inemavox: `~/projetos/inemavox/CLAUDE.md`, `api/server.py`, `api/job_manager.py`, `whisper_daemon.py`
- Opções do `claude -p`: `claude --help` desta máquina
- Placas e bibliotecas instaladas: `arduino-cli core list` e `arduino-cli board details -b esp32:esp32:XIAO_ESP32S3`

Não consegui ler: a ficha do INMP441 (a página devolveu só a capa) e preços em loja (a busca da loja depende de
JavaScript; limite já registrado em `~/projetos/wifi/LIMITES.md` em 14/11/2026).

## 15. O que ainda não foi verificado

- Nenhuma peça foi comprada nem medida. Toda medida NC é valor usual de mercado.
- Nenhuma transcrição nem voz foi gerada para este projeto. O tempo total de uma resposta não é conhecido.
  Só o `claude -p` foi medido: 5,0 s, uma vez.
- A pinagem da seção 9 é proposta. O único código compilado é o esqueleto que pisca o LED.
- O cubo de 40 mm é conta de empilhamento, sem modelo 3D.
- Compra no Brasil da XIAO ESP32S3 e do Atom Echo: não conferida.
