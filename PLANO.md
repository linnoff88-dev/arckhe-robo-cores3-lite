# PLANO — robo-cores3-lite

Cada fase tem um critério de pronto que se confere com um comando ou uma medida. O que cada parte é e por que foi
escolhida está na [DEFINICAO.md](DEFINICAO.md).

Ordem: a F1 não precisa de placa e começa já. A F0 (compra) corre em paralelo.

| Fase | O que entrega | Precisa de |
|---|---|---|
| F0 | CoreS3 Lite comprada e ligada | Nei |
| F1 | Servidor local responde a um WAV de teste, com e sem foto | Nada: só a máquina |
| F2 | Robô ouve e responde pela opção B, com rosto e legenda na tela | F0, F1 |
| F3 | Opção A: robô fala direto com uma API | F2 e **autorização do Nei** (serviço e finalidade) |
| F4 | Visão: foto na pergunta e "vídeo" em poucos quadros | F2 (opção B); F3 para o vídeo ao vivo |
| F5 | Guia e publicação | F2 e a ordem do Nei |
| F6 | Opcionais: suporte impresso, palavra de ativação, variante Waveshare | Decisão do Nei, um por um |

## F0 — Compra

O que fazer: comprar o item 1 da [LISTA-DE-COMPRAS.md](LISTA-DE-COMPRAS.md), conferindo que é a Lite (ou a completa),
com câmera.

Pronto quando:
- A placa chegou e liga pelo USB-C.
- `arduino-cli board list` mostra uma porta nova com a placa ligada.
- O preço pago em reais está na LISTA-DE-COMPRAS.md.

## F1 — Servidor local responde a um WAV de teste

**Pronta em 15/11/2026:** os 10 critérios passaram (tempos em `servidor/MEDIDAS.md`). Mudança de caminho: a
transcrição e a voz pela fila de jobs do inemavox levavam 12 s e 14–28 s; o servidor usa o Whisper residente do
inemavox e a voz residente `servidor/voz_residente.py`, que sobem sob demanda e saem depois de 10 min parados.

O que fazer: escrever `servidor/servidor.py` (só biblioteca padrão do Python) e `servidor/testar.py`, conforme
[servidor/README.md](servidor/README.md). Criar `servidor/teste/pergunta.wav` sem depender de ninguém: gerar
"que horas são em Tóquio?" pela rota `/api/jobs/tts/upload` do inemavox (voz `rachel`) e converter com
`ffmpeg -ar 16000 -ac 1 -c:a pcm_s16le`. Criar `servidor/teste/foto.jpg` (640 × 480) e
`servidor/teste/pergunta-visao.wav` ("o que você está vendo?").

Pronto quando, com o servidor no ar (`python3 servidor/servidor.py`):

| # | Comando | Saída esperada |
|---|---|---|
| 1 | `python3 servidor/testar.py servidor/teste/pergunta.wav` | Termina com `PASSOU` e código 0. Mostra `OUVIDO:`, `RESPOSTA:` e `TEMPOS:` |
| 2 | `ffprobe -v error -show_entries stream=codec_name,sample_rate,channels -of csv=p=0 servidor/teste/resposta.wav` | `pcm_s16le,16000,1` |
| 3 | o `testar.py` mede o volume da resposta com `ffmpeg -af volumedetect` | Volume médio acima de −40 dB |
| 4 | o `testar.py` transcreve a `resposta.wav` e compara com `X-Resposta` | 80% ou mais das palavras batem |
| 5 | `python3 servidor/testar.py --limites` | Token errado → 401. Fala de 2 MB → 413. Foto de 300 kB → 413. 3 s de silêncio → 204 sem chamar o Whisper. Arquivo que não é WAV → 415 |
| 6 | `python3 servidor/testar.py --foto servidor/teste/foto.jpg servidor/teste/pergunta-visao.wav` | `PASSOU`, e a `RESPOSTA:` cita algo que está na foto (conferido a olho) |
| 7 | `grep -rnE "https?://" servidor/*.py \| grep -v 127.0.0.1` | Nada: o servidor só fala com a própria máquina |
| 8 | `grep -rn "api/jobs/tts\"" servidor/*.py` | Nada: só a rota `/api/jobs/tts/upload` |
| 9 | `grep -n "tools" servidor/servidor.py` | O `claude -p` continua com `--tools ""`. Se a foto pedir outra coisa, parar e levar ao Nei |
| 10 | rodar o comando 1 três vezes seguidas | `PASSOU` nas três; o `total` de cada uma em `servidor/MEDIDAS.md` |

Meta de tempo: resposta de uma frase em até 20 s com os modelos carregados. É meta, não medida. Se passar de 20 s,
registrar onde o tempo foi gasto e levar ao Nei antes da F2.

## F1b — Amortecer a espera (pedido do Nei, 15/11/2026)

Pronta em 15/11/2026. Rota `/v1/conversa` por partes, `/v1/aquecer`, banca de 32 frases de espera na voz `rachel`.

| # | Comando | Resultado |
|---|---|---|
| 1 | `python3 servidor/testar.py --conversa servidor/teste/pergunta.wav` (5 vezes, com foto numa) | 1º som em 6,8 a 8,5 s (meta 8 s: 3 de 5 abaixo; antes, 10 a 14 s) |
| 2 | `python3 servidor/testar.py --conversa --frio servidor/teste/pergunta.wav` | 1º som 19,4 s depois do toque (meta 20 s; antes, 33 s) |
| 3 | 30 perguntas simuladas no `espera.Escolhedor` | Nenhuma frase repetida em 8 seguidas; 44% puladas; saudação sem frase |

Piso medido: a voz leva ~3 s até para uma frase curta e o Claude ~3,3 s; abaixo de uns 7 s não desce sem trocar a
voz. As animações do rosto ficam para a F2.

## F2 — O robô conversa pela opção B

O que fazer: instalar `M5Unified` e `M5GFX` (avisar o Nei antes: é download novo) e escrever o firmware em
`firmware/robo_fala/`: rosto, segurar para falar (chamando `/v1/aquecer` no toque), gravar, enviar por
`/v1/conversa`, tocar as partes e as frases de espera (banca baixada de `/v1/espera`), legenda.

Pronto quando:

| # | Comando ou ação | Saída esperada |
|---|---|---|
| 1 | `arduino-cli compile --fqbn esp32:esp32:m5stack_cores3 firmware/robo_fala` | Código 0 |
| 2 | Gravar e abrir o monitor serial | `PSRAM:` maior que zero, Wi-Fi conectado, `GET /saude` → 200 |
| 3 | Segurar o dedo na tela 3 s e dizer "um, dois, três, testando" a 50 cm, três vezes | O log do servidor mostra `OUVIDO:` com a frase certa nas três |
| 4 | `ffprobe` e `volumedetect` na gravação guardada pelo servidor | `pcm_s16le,16000,1`; volume médio acima de −35 dB; pico abaixo de 0 dB |
| 5 | Cinco perguntas seguidas, sem reiniciar | Cinco respostas tocadas até o fim, sem estalo, e o texto aparece na tela |
| 6 | Ouvir a 1 m, numa sala comum | Dá para entender todas as palavras |
| 7 | Tocar a tela durante a fala | A fala para em menos de 1 s e o robô volta a pronto |
| 8 | Segurar o dedo 20 s | A gravação para sozinha em 15 s e é enviada; a placa não reinicia |
| 9 | Desligar o servidor e falar | Rosto de erro por 2 s e volta a pronto; a placa não reinicia |
| 10 | 30 min parado e uma pergunta | Responde (o Wi-Fi reconecta sozinho) |

O tempo do dedo solto até o primeiro som vai para `servidor/MEDIDAS.md` nas cinco perguntas do teste 5.

## F3 — Opção A: direto numa API

Só começa depois de o Nei autorizar por escrito o serviço (Gemini Live, OpenAI Realtime) e a finalidade, e escolher
a variante A1 (direto) ou A2 (via servidor) — DEFINICAO.md, seção 10.

Pronto quando:

| # | Ação | Saída esperada |
|---|---|---|
| 1 | Trocar o cérebro em `segredos.h` e compilar | Código 0; o mesmo firmware serve às duas opções |
| 2 | Cinco perguntas seguidas | Cinco respostas; o tempo até o primeiro som fica em `servidor/MEDIDAS.md` ao lado da opção B |
| 3 | `grep -rn "API_KEY\|chave" firmware/robo_fala/*.ino` | Nenhuma chave no código; só no `segredos.h`, fora do git |
| 4 | Custo de uma conversa de 5 min, lido no painel da API | Anotado em `servidor/MEDIDAS.md` e mostrado ao Nei |

## F4 — Visão

Pronto quando:

| # | Ação | Saída esperada |
|---|---|---|
| 1 | Mostrar um objeto e perguntar "o que você está vendo?" (opção B) | A resposta nomeia o objeto em 4 de 5 objetos comuns |
| 2 | Medir o tempo a mais da foto | Anotado em `servidor/MEDIDAS.md` |
| 3 | Opção A com Gemini Live, se autorizada: "me avisa quando eu levantar a mão" | O robô avisa em 3 de 3 tentativas |

## F5 — Guia e publicação

Só com a ordem do Nei: criar o repo `inematds/robo-cores3-lite`, primeiro `git push`, guia em `guia/index.html`
(skill `projetos-landing-guia`, PT + `/en/` + `/es/`, tradução pelo `inema-traduz`), portal.

Pronto quando:
- O guia abre em `https://inematds.github.io/robo-cores3-lite/guia/` nos três idiomas.
- O revisor independente deu nota e a nota está registrada.
- O README tem a seção "O processo, do início ao fim" batendo com o que foi feito.
- O push entrou no `origin`. O Vercel não é conferido.

## F6 — Opcionais (um por um, só com decisão do Nei)

| Opcional | Critério de pronto |
|---|---|
| Suporte de mesa impresso | A placa encaixa inclinada, a tela fica legível a 1 m, o cabo USB-C passa. O pipeline de CAD está em `arquivo/variante-xiao/cad/README.md` |
| Palavra de ativação | 9 acertos em 10 tentativas a 1 m e nenhuma ativação falsa em 30 min de TV ligada. Modelo local novo: só com aprovação do Nei |
| Variante Waveshare 1,54" | Mesmo firmware, trocando só a camada de hardware; testes 1 a 10 da F2 passam |

## Riscos

| Risco | O que pode acontecer | Como se descobre cedo | Saída |
|---|---|---|---|
| Demora da opção B | Whisper + `claude -p` + Chatterbox somam mais de 20 s | F1, teste 10 | Whisper residente; resposta curta; rosto de "pensando"; levar o número ao Nei |
| Mic e falante no mesmo barramento | Troca lenta, estalo, falante mudo depois de gravar | F2, testes 5 e 7 | Pausa de 200–500 ms na troca; manter a ordem `end()` → `begin()` |
| Foto no `claude -p` | Sem ferramentas, o Claude não lê arquivo; a imagem pode não entrar | F1, teste 6 | Entrada stream-json com imagem; se exigir ferramenta, parar e levar ao Nei |
| Placa errada no compilador | A definição `m5stack_cores3` não serve à Lite ou a PSRAM fica em 0 | F2, teste 2 | Testar `PSRAM=opi`; ler o exemplo oficial da Lite |
| GPU ocupada | Rotinas na GPU atrasam a transcrição e a voz | F1, com a máquina em uso | Fila `fila-vaga gpu`; 503 com rosto de erro em vez de travar |
| Voz muda | O Chatterbox já entregou silêncio como sucesso | F1, teste 3 | O teste de volume barra |
| Número lido errado | O Chatterbox lê "2026" como "2006" | F1, teste 4 | A persona escreve número por extenso |
| Engine errada | Chamada de voz sem `engine` cai no Edge, online | F1, teste 8 | Só `/api/jobs/tts/upload` |
| Fala vira comando | Alguém tenta fazer o `claude -p` agir na máquina | F1, teste 9 | `--tools ""`, sem MCP, pasta vazia, sem sessão |
| Servidor aberto na rede | Outro aparelho manda áudio | F1, teste 5 | Token no cabeçalho |
| Chave da API no robô (A1) | Quem pegar o robô extrai a chave | F3 | Variante A2 (chave no PC) ou chave com limite de gasto |
| Custo da opção A | Conversa longa gasta mais que o esperado | F3, teste 4 | Medir antes de deixar ligado; limite de gasto na conta |
| Pastas de job acumulando | Cada turno cria pastas em `~/projetos/inemavox/jobs/` | F1, 20 turnos | Combinar com o Nei; não apagar nada do inemavox |
| Compra | Lite indisponível ou cara no Brasil | F0 | CoreS3 completa (mesma câmera, US$ 15 a mais) |
