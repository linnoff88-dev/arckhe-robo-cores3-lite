# Handoff — vídeos 9:16 de 3 assuntos nos lives (15/11/2026, ~04:20)

## Objetivo (pedido do Nei, 15/11 ~03:40)
Três assuntos em vídeos 9:16 curtos com o avatar do Nei, publicados pelo yt-pubx nos lives:
- Imersão Do chat ao agente às 12:00, refeita em 1ª pessoa: "eu vou estar", "minha visão estratégica".
- Os 5 níveis de IA às 16:00 (escada AL1–AL5, a análise vira plano de evolução).
- Do zero ao Jarvis às 08:00 (conteúdo grátis que ele fez este mês no inema.club, com kit passo a passo).
- "Amanhã é hoje": publicar hoje (15/11), segunda (16/11) e terça (17/11).

## Decisões do Nei (literais na CONTINUAR.md)
- **Canais (15):** lives1–4, 6–9, 11, 12, 22, 23, 24, 31, 32. lives5 e lives10 ficam fora.
- **Cada vídeo sai UMA vez no YouTube:** cada canal recebe um vídeo diferente. O mesmo vídeo pode ir a outra plataforma da marca (TikTok/Insta). Está na memória `canais-conteudo-diferente`.
- **Leitura proposta, ainda SEM confirmação do Nei:** 45 vídeos ao todo. Cada canal recebe 3, um por dia, um de cada assunto. Cada dia, 5 canais recebem cada assunto, e os grupos rodam entre os dias. A outra leitura (135 vídeos) não cabe até terça.

## Feito
- **Imersão:** os 01–07 de `~/projetos/output/promo-imersao` estão refeitos em `~/projetos/output/promo-imersao-v2/` (fala.txt, roteiro.yaml dos cards e legenda.txt em 1ª pessoa).
  - Os 7 avatares foram mandados ao estúdio HeyGen pelo `_avatares/lote.sh`, que baixa sozinho para `NN-*/avatar.mp4`.
  - O 08, o 09 e o 10 originais já estavam em 1ª pessoa: reaproveitar.
- **Níveis e Jarvis:** 6 fichas r7ex em `~/projetos/r7ex/edicoes/2026-11-15-*`, todas aprovadas no D15 e com avatar enviado:

| Ficha | video_id | Ângulo |
|---|---|---|
| niveis-ia | 675c1a93… | os 5 níveis |
| niveis-ia-v2 | ef2f9d2b… | quando soltar e quando puxar de volta |
| niveis-ia-v3 | 5727549b… | 64%, medição do Nei no ESCADA.md |
| zero-ao-jarvis | ebea7bd8… | as 6 etapas |
| zero-ao-jarvis-v2 | 40e3e711… | um agente em 87 linhas |
| zero-ao-jarvis-v3 | 8dff6fe5… | só faz o perigoso com o seu OK |

- **Vigia:** `continua.py --add` com o nome imersao-v2 (msg 4787 no v3) confere os 7 avatar.mp4 da imersão. A fase 2 segue `promo-imersao-v2/CONTINUAR.md`.
- **Registros:** uma linha nova no `~/projetos/r7ex/FALHAS.md` (card do HeyGen ficou Draft; repetir o envio resolveu).
- **Vídeo de referência** C45VVcCV9OY (baixado e transcrito em `~/projetos/output/ref-C45VVcCV9OY/`): NÃO é parecido. É Fable 5.2 × Opus 5.5 com 8 regras de prompt.

## Pela metade / próximo
1. **Montar a imersão** quando os avatar.mp4 chegarem (previsão ~05:10): cards 01–05 (cardshorts cards + `promo-imersao/compor.py`) e 06–07 (`_motor/monta06/07.py`). Conferir os caminhos e olhar os quadros (nenhuma criança).
2. **Montar as fichas r7ex** à mão: `python3 r7ex.py fazer <pasta>`, depois LER `build/folha.jpg`. **NUNCA** `producao.py --add` nem `fila`: os dois mandam para a fila do lives7.
3. **Agendar no yt-pubx** depois que o Nei confirmar a conta dos 45. Exemplo: `./yt-pubx publicar <mp4> --canal livesN --contexto "..." --agendar "AAAA-MM-DD HH:MM"`.
   - Um canal por vídeo.
   - Atenção ao limite de cerca de 4 envios por dia por canal.
   - Hoje às 08:00 provavelmente atrasa; publicar assim que ficar pronto.
4. **Faltam 29 vídeos** para fechar 45, se o Nei confirmar: imersão +5, níveis +12, Jarvis +12.

## Não fazer
- Não mexer no plano do Metricool de 12–21/11 (versões antigas em 3ª pessoa) sem o Nei.
- Nenhuma API fora do estúdio HeyGen e do yt-pubx.
- Não burlar o portão D15.
- Não publicar no lives10 nem no lives5.

## Pergunta em aberto ao Nei
"São 45 vídeos (cada canal recebe 3, um por dia, um de cada assunto)?"


<!-- handoff-estado:inicio -->
## Estado gravado pelo script (não editar)

Gravado por handoff-grava.py no momento do handoff. `--conferir` compara com o projeto agora.

- commit: ca93d6dc299a9e50c5ef53e1df085775cce6eed0 · branch: main
- arquivos sujos fora de handoffs/: 0
<!-- handoff-estado:fim -->
