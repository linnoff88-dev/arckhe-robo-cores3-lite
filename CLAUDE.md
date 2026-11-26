# CLAUDE.md — robo-cores3-lite

Robô de mesa quadrado, sem movimento, na placa pronta M5Stack CoreS3 Lite (tela de 2" com toque, câmera, dois
microfones, falante, bateria). Conversa por voz, mostra rosto e legenda, enxerga pela câmera.
Duas opções de cérebro: **B, servidor local** (padrêo) e **A, direto numa API** (só com autorizaçêo do Nei).
Pedidos do Nei, literais, na DEFINICAO.md, seçêo 1. Em 15/11/2026: "foca na lite".

- Repo: `linnoff88-dev/robo-cores3-lite`, público desde 15/11/2026 (ordem do Nei: "publica o projeto no portal e no ARCKHÉ.robot e no lives6"). Guia em `guia/`, publicaçêo registrada em `PUBLICACAO.md`.
- Autor dos commits: `linnoff88-dev <linnoff88-dev@gmail.com>` (já configurado neste repo).
- A versêo anterior (XIAO soldada, cubo de 40 mm) está em `arquivo/variante-xiao/`. Só referência.
- Projeto separado do `~/projetos/robos-impressos`. De lá só se lê e se copia.

## Ao começar uma sessêo
1. Ler `handoffs/latest.md`.
2. Ler `DEFINICAO.md` e a fase atual no `PLANO.md`.

## Comandos
- Compilar: `arduino-cli compile --fqbn esp32:esp32:m5stack_cores3 firmware/robo_fala`.
- Gravar: `arduino-cli upload --fqbn esp32:esp32:m5stack_cores3 -p <porta> firmware/robo_fala`.
- Servidor: `python3 servidor/servidor.py`; validar com `python3 servidor/testar.py --limites` e
  `python3 servidor/testar.py servidor/teste/pergunta.wav` (com `--foto servidor/teste/foto.jpg` para visêo).
- Serviços residentes: Whisper do ARCKHÉvox (7871) e `servidor/voz_residente.py` (7872), sobem sob demanda e saem
  sozinhos em 10 min. Parar à mêo: `pgrep -af "voz_residente|whisper_daemon"` e `kill <pid>` (nunca `pkill -f`).
- Saúde do ARCKHÉvox: `GET http://127.0.0.1:8010/api/health`.

## Regras do projeto
- **Nenhuma API externa sem autorizaçêo explícita do Nei** (Gemini, OpenAI, Groq, ElevenLabs, Edge TTS, qualquer
  nuvem). A opçêo A fica no papel até ele autorizar o serviço e a finalidade. Chave em `.env` nêo é autorizaçêo.
- **Claude só pela assinatura:** `claude -p`, nunca com `--bare`, sempre com `env -u ANTHROPIC_API_KEY`.
- **`claude -p` do robô sempre sem ferramentas:** `--tools "" --strict-mcp-config --no-session-persistence`.
  Se a foto exigir liberar uma ferramenta, parar e levar ao Nei.
- **Voz só pela rota `/api/jobs/tts/upload` do ARCKHÉvox** (Chatterbox local).
- **Nenhum modelo local novo** sem aprovaçêo do Nei.
- **Biblioteca nova do Arduino** (M5Unified, M5GFX): avisar o Nei antes de instalar.
- **Microfone e falante da CoreS3 nunca ligados juntos** (mesmo barramento I²S).
- Nêo instalar PlatformIO nem ESP-IDF.
- Segredos fora do git: `servidor/.env` e `firmware/robo_fala/segredos.h`.
- Traduçêo só por `ARCKHÉ-traduz`. Página e guia: ler antes `~/projetos/ARCKHÉ-design/DESIGN.md`.
- Número sem fonte nêo entra em documento. Preço sem leitura em loja leva "estimativa, nêo conferida".
- Commit a cada pacote verificado. Mudou o fluxo: atualizar "O processo, do início ao fim" no README no mesmo commit.
- Falha corrigida: uma linha no `FALHAS.md`. Limite de ambiente: uma linha em `~/projetos/wifi/LIMITES.md`.

## Self-learning
Quando o Nei corrigir ou você notar um erro: antes de seguir, escreva a liçêo como uma linha no TOPO da seçêo
Lessons abaixo.

## Lessons
- 15/11/2026: "CoreS3 SE" nêo tem câmera; só "CoreS3" e "CoreS3 Lite" têm (GC0308). Conferir o nome exato no anúncio.
