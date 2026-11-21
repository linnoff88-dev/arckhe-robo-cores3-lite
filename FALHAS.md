# FALHAS

Uma linha por falha, a mais recente no topo. Limite de ambiente (ferramenta, permissão, cota) vai em
`~/projetos/wifi/LIMITES.md`, não aqui.

| data | o que quebrou | menor correção | prompt \| infra |
|---|---|---|---|
| 15/11/2026 | Banners do guia: selo "CoreS3 Lite" por cima do subtítulo (grade), "ROBOT TALKING" fora de ordem (EN), "computadiora" (ES) | Conferir cada banner com Read e gerar de novo só o errado; grade sem `--selo` | prompt |
| 15/11/2026 | Capa do catálogo saiu com robô fofo de braços e olhos de emoji (proibido pela V12 e falso: o robô é uma placa quadrada) | `gerar-capa.cjs --raw-in` com recorte da placa do banner, sem nova geração | prompt |
