# firmware — o programa da CoreS3 Lite

**Hoje só existe o esqueleto:** `robo_fala/robo_fala.ino` mostra o tamanho da PSRAM pela serial. Ele compila
para a placa `m5stack_cores3` (conferido em 15/11/2026: 300 492 bytes, 9% do espaço). Não foi gravado numa placa:
ela ainda não chegou. Rosto, voz e câmera entram nas fases F2 a F4 do [PLANO.md](../PLANO.md).

## Ferramenta: Arduino pelo `arduino-cli`

- Core `esp32:esp32` 3.3.12, já instalado. A placa `M5CoreS3` (`esp32:esp32:m5stack_cores3`) já existe nele.
- PSRAM: a placa vem com `PSRAM=enabled` (QSPI) por padrão, lido no `boards.txt`. **Não verificado na Lite.**
  Se a serial mostrar `PSRAM: 0`, compilar com `:PSRAM=opi`.
- Bibliotecas da F2: `M5Unified` e `M5GFX` (tela, toque, microfone, falante, energia). **Não instaladas:**
  `arduino-cli lib install M5Unified M5GFX` é download novo, avisar o Nei antes.
- Câmera (F4): `esp_camera`, que já vem no core (`espressif__esp32-camera`). A M5Unified não cuida da câmera.

## Comandos

```
# compilar (na raiz do repo)
arduino-cli compile --fqbn esp32:esp32:m5stack_cores3 firmware/robo_fala

# descobrir a porta da placa
arduino-cli board list

# gravar
arduino-cli upload --fqbn esp32:esp32:m5stack_cores3 -p /dev/ttyACM0 firmware/robo_fala

# ver as mensagens
arduino-cli monitor -p /dev/ttyACM0 -c baudrate=115200
```

Gravar e monitor: não testados, sem placa.

## Segredos

Copie `robo_fala/segredos.exemplo.h` para `robo_fala/segredos.h` e preencha Wi-Fi, servidor, token e o cérebro
escolhido. O `segredos.h` está no `.gitignore`.

## O que o firmware vai fazer

Duas camadas, para a variante Waveshare poder entrar depois trocando só a de baixo:

| Camada | O que faz | Implementações |
|---|---|---|
| Cérebro | Manda a fala (e a foto) e recebe a resposta | `servidor` (opção B, HTTP) · `api` (opção A, WebSocket; só com autorização do Nei) |
| Hardware | Tela, toque, microfone, falante, câmera | CoreS3 Lite (M5Unified + esp_camera) · depois, se pedido, Waveshare 1,54" |

Fluxo da opção B (rota `/v1/conversa`, por partes; DEFINICAO.md, seção 11):
0. Ao ligar: baixa a banca de frases de espera (`GET /v1/espera`) se mudou.
1. Liga, conecta no Wi-Fi, chama `GET /saude`, mostra o rosto.
2. Dedo na tela: chama `POST /v1/aquecer`, liga o microfone e grava na PSRAM (16 kHz, 16 bits, mono), até 15 s.
3. Dedo solto: desliga o microfone, manda a foto se houver (`POST /v1/foto`) e o WAV (`POST /v1/fala`).
4. Quadros: `O` → mostra "Você disse"; `E` → toca a frase de espera da memória; `T`/`A` → legenda e toca cada parte.
   Toque na tela durante a fala: para.

Estados: `PRONTO` → `OUVINDO` → `PENSANDO` → `FALANDO` → `PRONTO`. Falha: `ERRO` por 2 s.

## Pontos de atenção

- **Microfone e falante dividem o mesmo barramento I²S** na CoreS3. Nunca ligados juntos: `M5.Mic.end()` antes de
  `M5.Speaker.begin()` e o contrário, com uma pausa de 200 a 500 ms (DEFINICAO.md, seção 6).
- O programa só usa Wi-Fi de 2,4 GHz.
