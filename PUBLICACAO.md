# PUBLICACAO — robo-cores3-lite

Ordem do Nei (15/11/2026): "publica o projeto no portal e no inema.robot e no lives6".
Guia, portal e Telegram: feitos aqui. Vídeo no lives6: outro agente (ele lê este arquivo para responder no mesmo
tópico do Telegram).

portal: feito
telegram: feito 2986
lives6: feito https://www.youtube.com/watch?v=ckhcNbClXNs

## Guia (GitHub Pages, via Actions, branch main)

| Idioma | URL |
|---|---|
| PT | https://inematds.github.io/robo-cores3-lite/guia/ |
| EN | https://inematds.github.io/robo-cores3-lite/guia/en/ |
| ES | https://inematds.github.io/robo-cores3-lite/guia/es/ |

- As três responderam 200 em 15/11/2026 às 02:01 (e a raiz, que redireciona para `guia/`).
- Repo: https://github.com/inematds/robo-cores3-lite · commit do guia `27ba4c8`.
- O guia tem a marca `<!-- VIDEO: entra o explicavideo do projeto quando publicado -->` nos 3 idiomas, logo
  depois do `#resumo`: o vídeo do lives6 entra ali (e uma linha "🎬 Vídeo:" nos 3 READMEs).
- Revisor independente: 6 rodadas (6, 6, 7, 7, 7 reprovado; 6ª aprovado, nota 8), notas em
  `~/projetos/wifi/scripts/revisor-nota.py`.

## Portal (skill atualiza-portal)

| Repo | Commit |
|---|---|
| NeiMaldaner/portal (inema.club) | `0d20e49` |
| inematds/inemabuscas | `cb0147c` |
| inematds/inemapro (inemapro-mono, catálogo PRO) | `e625bad` |

- Card em `communityProjects` (badge Guia), topo de `projectUpdatesData`:
  "robo-cores3-lite — robô de mesa que conversa por voz, sem pagar API por pergunta".
- EN/ES em `translated-courses.ts` (id 10231). Enrichment `projeto:robo-cores3-lite-guia` (robotica-ia-fisica).
- No inema.club aparece só no quadro "Últimas Atualizações de Projetos"; no PRO entra no catálogo e na busca.

## Telegram (grupo INEMA.ROBOT)

- Tópico: **2986** — https://t.me/c/2412734678/2986
- Título: "Robô de mesa que conversa - Sua voz não sai de casa e você não paga API por pergunta"
- Mensagens 2987 a 3001; lançado no MENU (https://t.me/c/2412734678/2270, msg 3002).
- Texto: `~/projetos/output/posts-telegram/2026-11-15-robo-cores3-lite.md`; capa:
  `~/projetos/output/posts-telegram/capas/robo-cores3-lite.jpg`.
- Para responder no mesmo tópico: `postar_topico.py --grupo INEMA.ROBOT --topico 2986 ...` (skill `postar-telegram`).
- Nada no Telegram pode ser apagado sem aprovação individual do Nei.

## Vídeo (lives6)

- YouTube (INEMA Robot, lives6, público, Short): https://www.youtube.com/watch?v=ckhcNbClXNs
- Título: "Essa placa de R$ 256 vira um robô que conversa (e não paga API) #shorts"
- Reel r7ex, 58,6 s, 9:16. MP4: `~/projetos/r7ex/edicoes/2026-11-15-robo-cores3-lite/video.mp4`
  (folha `build/folha.jpg`; revisor independente: aprovado, impacto 7, só sugestões).
- Publicado direto com o yt-pubx em 15/11/2026 02:49 (exceção de 05/11: a entrega precisava do link); não entrou na fila.
- v3: msg 4779. Telegram: resposta no tópico 2986, msgs 3023–3024 — https://t.me/c/2412734678/3024
- Guia: seção `#video` (embed vertical) nos 3 idiomas; linha "🎬 Vídeo" nos 3 READMEs.
- Portal: quadro "Últimas Atualizações de Vídeos" + série de shorts em /videos/ (portal `162d5d9`); MP4 na release
  https://github.com/inematds/robo-cores3-lite/releases/tag/video-v1.0.0
