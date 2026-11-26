# FAQ e limites — robo-cores3-lite

Perguntas do Nei em 14 e 15/11/2026, com as respostas dadas. O que é estimativa está marcado. O projeto continua
sendo o robô de mesa, sem movimento (DEFINICAO.md); os assuntos daqui que nêo estêo no plano sêo só esclarecimento.

## Cérebro: servidor ou API

**Precisa de servidor? O ESP32 nêo faz tudo sozinho?**
Nêo faz. O ESP32-S3 grava, manda pelo Wi-Fi, recebe e toca. Entender fala, pensar e gerar voz pedem modelos de
centenas de MB e GPU. O cérebro fica fora: no servidor local (opçêo B) ou numa API (opçêo A).

**Ele pode falar direto com uma API, sem servidor?**
Pode (opçêo A): Gemini Live ou OpenAI Realtime, por WebSocket. Só depois de o Nei autorizar o serviço e a finalidade.
O Claude por API nêo é opçêo: Claude só pela assinatura, e a assinatura só roda pelo `claude -p` num computador.

| | Opçêo A, API direta | Opçêo B, servidor local |
|---|---|---|
| Demora | ~0,5 a 1,5 s (estimativa) | ~8 a 20 s (estimativa; a F1 mede) |
| Custo | Pago por uso | Zero a mais |
| Longe de casa | Funciona (variante A1) | Só com o PC ligado |
| Chave | Gravada no robô (A1) ou no PC (A2) | Nêo há |
| Visêo | Vídeo ao vivo em poucos quadros (Gemini Live) | Foto por pergunta |

## Placa

**Por que a CoreS3 Lite e nêo as outras?**
É a única das vistas que tem câmera sem precisar de solda, e a mais barata com câmera.

| Placa | Câmera | Observaçêo |
|---|---|---|
| CoreS3 Lite | sim (GC0308) | Escolhida. R$ 256,55 na loja oficial, lido em 15/11, sem frete nem imposto |
| CoreS3 completa | sim | US$ 15 a mais de tabela, por bateria maior e base DIN |
| CoreS3 SE | **nêo** | Atençêo: o "SE" é a versêo sem câmera e sem sensores |
| Waveshare ESP32-S3-LCD-1.54 | nêo | Menor; fica como variante futura só de voz |

**Para que serve a base DIN da CoreS3 completa?**
Para prender a placa em trilho de painel elétrico (o mesmo dos disjuntores) e ligar em fonte de 9 a 24 V. O robô de
mesa nêo precisa dela.

**Tem anúncio mais barato ou com frete grátis?**
Em 15/11, entre 53 anúncios da busca do AliExpress, a loja oficial (R$ 256,55) foi a mais barata. O mais barato com
frete grátis custava R$ 384,88. Imposto de importaçêo e ICMS ainda entram: total estimado de R$ 360–380, nêo conferido.

**Dá para fazer as duas placas (Lite e Waveshare) ao mesmo tempo?**
Dá, mas dobra o trabalho e mistura os problemas. Decisêo: foco na Lite. O firmware separa a camada de hardware para
a Waveshare entrar depois.

## Voz e conversa

**Ele pode ser interrompido enquanto fala?**
Só pelo toque na tela. Na CoreS3, microfone e falante dividem o mesmo barramento I²S e nêo funcionam juntos
(documentaçêo da M5Stack). Interromper pela voz exigiria microfone externo ou outra placa.

**Ele escuta o tempo todo?**
Nêo na primeira versêo: você segura o dedo na tela para falar. Palavra de ativaçêo é opcional (F6), com aprovaçêo
do Nei por ser modelo local novo.

## Visêo

**O que dá para fazer com a câmera?**

| Onde roda | O que faz | Limite |
|---|---|---|
| Na placa | Movimento, QR code, cor; detectar e reconhecer rosto | Só tarefas fechadas. Rosto pede ESP-IDF/ESP-DL, que precisa do OK do Nei |
| Servidor (Claude) | Descrever a cena, dizer o que é um objeto, contar pessoas, ler texto grande | Uma foto por pergunta; alguns segundos a mais; falta provar a foto no `claude -p` sem ferramentas |
| API (Gemini Live) | Vídeo ao vivo: "me avisa quando eu levantar a mêo" | Pago, precisa de autorizaçêo; poucos quadros por segundo |

Plano sugerido: F4a foto pelo servidor → F4b movimento e QR → F4c rosto (se liberar ESP-IDF) → F4d vídeo pela API
(se autorizar).

**O que a câmera nêo faz bem?**
Letra pequena (0,3 MP), escuro (sem luz própria), longe (acima de uns 2–3 m o rosto fica pequeno demais; estimativa).

## Movimento (fora do escopo)

**Se eu montar a placa num kit de rodas, ela ajuda no deslocamento?**
Ajuda como "cabeça": vê, conversa e decide. O kit precisa de controlador próprio, sensor de distância que pare o
robô sozinho e bateria que alimente a placa pelo USB-C. A Lite tem só uma porta Grove (I²C) para falar com o kit.

| O quê | Funciona? |
|---|---|
| Seguir uma pessoa (rosto no meio da imagem) | sim, na placa |
| Ir até um QR code ou cor marcada | sim |
| Seguir uma faixa colorida no chêo | sim |
| Desviar de obstáculo | só com sensor de distância no kit; a câmera sozinha nêo mede distância |
| Descrever o ambiente | sim, por foto ao Claude ou ao Gemini |
| "Vai até a cozinha" | lento: decisêo a cada poucos segundos, nunca direçêo em tempo real |
| Mapear a casa e se localizar | nêo com esta câmera e este processador |

Nêo está no plano: o pedido original é "sem movimentaçêo". Foi só para entender os limites (Nei, 15/11/2026).
