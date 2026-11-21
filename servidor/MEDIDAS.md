# MEDIDAS — tempos do servidor (opção B)

Segundos. stt = Whisper residente, llm = claude -p, tts = voz residente.

| quando | teste | foto | stt | llm | tts | total | ouvido |
|---|---|---|---|---|---|---|---|
| 15/11/2026 00:49:38 | pergunta.wav | não | 0.7 | 5.2 | 5.2 | 11.3 | Que horas são em Tóquio? |
| 15/11/2026 00:49:56 | pergunta-visao.wav | sim | 0.4 | 4.2 | 11.2 | 15.9 | O que você está vendo? |
| 15/11/2026 00:50:21 | pergunta.wav | não | 1.2 | 5.7 | 6.7 | 13.8 | Que horas são em Tóquio? |
| 15/11/2026 00:50:34 | pergunta.wav | não | 0.6 | 4.4 | 6.6 | 11.6 | Que horas são em Tóquio? |
| 15/11/2026 00:50:46 | pergunta.wav | não | 0.5 | 4.3 | 5.3 | 10.1 | Que horas são em Tóquio? |
| 15/11/2026 00:51:39 | pergunta.wav | não | 12.4 | 4.6 | 16.1 | 33.2 | Que horas são em Tóquio? |

Notas (15/11/2026):
- As linhas de 00:49 a 00:50 são com os serviços residentes já no ar ("quente"): **10,1 a 13,8 s** sem foto,
  15,9 s com foto (a resposta com foto foi mais longa: a voz demora mais).
- A última linha é "fria": Whisper e voz residentes desligados antes, subidos pelo servidor no próprio turno
  (whisper 12,4 s, voz 16,1 s): **33,2 s**. Acontece na primeira pergunta depois de 10 min parado.
- Antes dos serviços residentes, pela fila de jobs do inemavox: transcrição 12,1 s e voz de 14 a 28 s por frase.
- A voz cresce com o tamanho da resposta (~1,3 a 1,8 s de geração por segundo de fala).
| 15/11/2026 01:20:04 | conversa pergunta.wav | não | 0.52 | 4.69 | 8.45 | 13.72 (1º som 7.26) | hora-04 |
| 15/11/2026 01:20:16 | conversa pergunta.wav | não | 0.53 | 4.9 | 5.54 | 11.01 (1º som 7.57) | hora-04 |
| 15/11/2026 01:22:54 | conversa pergunta-visao.wav | sim | 0.42 | 3.68 | 7.96 | 12.12 (1º som 6.88) | foto-01 |
| 15/11/2026 01:24:13 | conversa pergunta.wav | não | 0.49 | 3.3 | 6.04 | 9.89 (1º som 6.79) | - |
| 15/11/2026 01:25:04 | conversa pergunta-visao.wav | sim | 0.43 | 4.81 | 9.08 | 14.37 (1º som 7.37) | - |
| 15/11/2026 01:25:15 | pergunta.wav | não | 0.5 | 4.0 | 5.3 | 9.9 | Que horas são em Tóquio? |
| 15/11/2026 01:25:46 | conversa fria pergunta.wav | não | 7.48 | 4.75 | 9.88 | 22.15 (1º som 15.79) | frio-04 |

Notas da F1b (15/11/2026, /v1/conversa): "1º som" = do envio até o primeiro áudio da resposta. Quente: 6,8 a 7,6 s nas seis linhas da tabela (o PLANO.md registra até 8,5 s em rodadas que não viraram linha aqui).
Frio com /v1/aquecer chamado no toque e 3,6 s de fala: 15,8 s depois do envio, 19,4 s depois do toque. A frase de
espera, quando sai, chega em ~0,6 s (ou na hora, no caso frio).
| 15/11/2026 01:42:24 | conversa pergunta-visao.wav | sim | 0.42 | 4.1 | 8.86 | 13.41 (1º som 7.36) | foto-04 |
