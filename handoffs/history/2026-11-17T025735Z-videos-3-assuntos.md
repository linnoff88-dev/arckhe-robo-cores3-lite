# Handoff — vídeos 9:16 de 3 assuntos nos lives (lote-135), 16/11/2026 ~23:20

## Objetivo (pedido do Nei, 15/11)
3 assuntos (imersão em 1ª pessoa "comigo/eu vou estar/minha visão estratégica", 5 níveis de IA, do zero ao Jarvis), shorts 9:16 r7ex com avatar HeyGen e imagens Codex. Cada canal lives recebe 3 vídeos por dia (Jarvis 08:00 · imersão 12:00 · níveis 16:00) em 15, 16 e 17/11. **Cada vídeo sai UMA vez no YouTube** (memória `canais-conteudo-diferente`). Canais: lives1–4, 6–9, 11, 12, 22, 23, 24, 31 (lives5 e lives10 fora por ordem do Nei; lives32 fora por OAuth 401).

## Estado (16/11 23:15)
- Agendados (`~/projetos/output/lote-135/publicados.tsv`, 100 linhas): 15/11 42/42, 16/11 42/42, 17/11 16/42 (Jarvis 8, imersão 1, níveis 7).
- Faltam 26 para 17/11; já montados: imersão 16 (precisa 13), níveis 7 (precisa 7), Jarvis 5 + 2 recém-consertados (p11 manchete "NOITES PERDIDAS COM IA", p42 capa refeita por falta de acento) (precisa 6).
- Sobem depois da meia-noite: agendador tem teto de 4 envios/canal/dia para vídeo de outro dia.
- Processos em segundo plano (setsid): `montador3.sh` (níveis→imersão→Jarvis), `agendador.py` (revisor claude -p + publicar.sh/yt-pubx, conserto automático de manchete cortada), `reenviador.sh` (HeyGen deslogado). Trabalhadores de roteiro encerrados.
- Detalhes, comandos de parar e correções: `~/projetos/output/lote-135/LEIA.md`.

## Pendente / próximo
1. Conferir após 00:00 de 17/11 que os 26 de terça foram agendados (`awk -F'\t' '{split($4,a," "); print a[1],a[2]}' publicados.tsv | sort | uniq -c`).
2. **Bug a corrigir:** o revisor (`claude -p`) falhou ~12.600 vezes com "substring not found" (15/11 10:45 → 16/11 20:56, provável limite da assinatura) e o agendador repetia a cada 5 min por vídeo. Pôr recuo (backoff) no `agendador.py` quando o revisor falhar; registrar no FALHAS.md do r7ex.
3. Níveis p07 e p23 com `.montagem-falhou` (não fazem falta; níveis tem sobra).
4. lives32: Nei precisa rodar `cd ~/projetos/yt-pubx && ./yt-pubx auth lives32`; depois devolver o canal à lista CANAIS do `agendador.py` (há vídeos de sobra). Registrado em `~/projetos/wifi/LIMITES.md`.
5. Depois de 17/11: parar os processos (`touch PARAR_AGENDADOR PARAR_MONTADOR PARAR_REENVIADOR` em lote-135).
6. Plano Metricool de 12–21/11 (`wifi/promo-imersao/plano.json`) ainda usa versões em 3ª pessoa da imersão: não mexer sem o Nei.

## Correções feitas no r7ex (não commitadas; repo r7ex tinha outras mudanças pendentes)
- `r7ex/retempo.py`: `_tapa_buracos` buraco 8→3 s e 3 recortes por buraco (Whisper instável na borda).
- FALHAS.md do r7ex: linhas de 15/11 (cauda 6 s, retempo, manchete de 3 linhas, Draft do HeyGen).

## Não fazer
- Não publicar o mesmo arquivo em dois canais; não publicar em lives5/lives10; não forçar o crítico D15; não trocar plano do HeyGen.


<!-- handoff-estado:inicio -->
## Estado gravado pelo script (não editar)

Gravado por handoff-grava.py no momento do handoff. `--conferir` compara com o projeto agora.

- commit: a0d756dd6bdb505a052939475dc03a5f2a70b195 · branch: main
- arquivos sujos fora de handoffs/: 0
<!-- handoff-estado:fim -->
