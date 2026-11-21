# cad — a caixa do robô

> **Arquivado em 15/11/2026.** O projeto trocou para a placa pronta M5Stack CoreS3 Lite (ver `../../../DEFINICAO.md`).
> Este arquivo descreve a variante antiga, XIAO ESP32S3 soldada num cubo impresso de 40 mm. Só referência.

**Hoje só existe a conta do tamanho.** O modelo 3D da caixa é a fase F4 do [PLANO.md](../PLANO.md).

| Arquivo | O que é |
|---|---|
| `parametros.py` | Todas as medidas, cada uma com a fonte (P, T ou NC) |
| `caixa_minima.py` | Calcula o menor cubo a partir das medidas. Só biblioteca padrão do Python |

```
python3 cad/caixa_minima.py              # parede de 2,0 mm
python3 cad/caixa_minima.py --parede 2.4
```

Resultado em 14/11/2026, com parede de 2,0 mm: mínimo de 37,0 mm, alvo de **40 mm** (variante A). Mudou uma medida em
`parametros.py`? Rode de novo e atualize a seção 12 da [DEFINICAO.md](../DEFINICAO.md) no mesmo commit.

## Como reaproveitar o pipeline do robos-impressos (F4)

O `~/projetos/robos-impressos` tem um pipeline de CAD em Python (trimesh + manifold3d) que gera as peças, confere
com 11 testes e faz os renders. A ideia é **copiar** o que serve para cá, não depender da outra pasta.

**Copie de um commit, não da pasta de trabalho.** Em 14/11/2026 a pasta `comum/cad/` de lá tinha mudanças sem
commit de uma sessão em andamento. O commit de referência é `aef010a`:

```
mkdir -p /tmp/cad-robos && git -C ~/projetos/robos-impressos archive aef010a comum/cad requirements.txt | tar -x -C /tmp/cad-robos
```

| Arquivo de lá (`comum/cad/`) | Serve para | Trazer? |
|---|---|---|
| `comum/geo.py` | Formas: caixa, cilindro, união, ressalto com nervura, retângulo arredondado | Sim |
| `comum/modelo.py` | Classes `Peca`, `Comp`, `Junta`, `Modelo` | Sim |
| `comum/componentes.py` | Envelopes dos componentes comprados (entram no teste de interferência e nos renders) | Sim, como molde: escrever os envelopes da XIAO, do amplificador, do microfone, do falante e do botão |
| `comum/imprimibilidade.py` | Testes 10 e 11: áreas sem apoio, pontes | Sim |
| `comum/quadrado.py` | Os robôs quadrados (cubo e cubo que roda) | Só como referência de estilo: tem servo, pescoço e tela |
| `gerar.py` | Exporta STL, 3MF, mesas de impressão, `montagem.json` | Sim |
| `verificar.py` | Os 11 testes, lidos dos arquivos exportados | Sim |
| `caminhos.py` | Registro dos robôs e das pastas | Sim, adaptado: aqui há um modelo só |
| `parametros.py` | Medidas | Só as seções IMPRESSORA, FOLGAS e IMPRESSAO_LIMITES, coladas no `parametros.py` daqui |
| `depurar.py`, `onde.py` | Volume e caixa de cada peça; onde duas peças se sobrepõem | Sim |
| `render_blender.py`, `renders.sh`, `vistas.sh` | Renders pelo Blender | Sim, na hora do guia (F5) |
| `bicho.py`, `casca.py`, `base.py`, `base_baixa.py`, `peles/`, `pele_malha.py`, `imagem3d.py`, `comparar.py`, `tabelas.py` | Bichos, peles, image-to-3D, tabelas dos 4 robôs | Não |

O que adaptar (não testado: a sessão da F4 confere antes de copiar):
- `caminhos.py` assume a estrutura `comum/cad/` + `projetos/<robô>/` e calcula a raiz do repo por ela. Aqui o pacote
  fica em `cad/` e há um robô só.
- `gerar.py`, `verificar.py` e `imprimibilidade.py` importam `cad.parametros` e `cad.caminhos`.
- Ambiente: `python3 -m venv .venv && .venv/bin/pip install -r requirements.txt` com o `requirements.txt` de lá
  (trimesh 5.2.1, manifold3d 3.5.5 e os demais). É instalação: fazer na F4, não antes.

Os 11 testes do `verificar.py` (lidos no cabeçalho do arquivo): 1 contagem de peças, 2 malha fechada, 3 cabe na mesa
de 256 mm, 4 parede de 2,0 mm ou mais, 5 interferência entre peças e componentes, 6 teste negativo do 5, 7 peça solta,
8 equilíbrio, 9 caminho de montagem, 10 imprimibilidade sem suporte, 11 teste negativo do 10.

## Regras da caixa

- Cabe na Bambu Lab A1 (256 × 256 × 256 mm): com 40 mm, sobra.
- Parede de 2,0 mm ou mais. Sem suporte sempre que der. Reforço onde há carga (postes dos parafusos, anel do falante).
- Toda medida de componente fica em `parametros.py`, com a fonte. Nenhum número solto no desenho.
- Antes de imprimir a caixa, imprimir a peça de teste (abertura do USB-C, anel do falante, poste do parafuso, tecla).

## Peças previstas

| Peça | O que é | Como imprime |
|---|---|---|
| `casca` | 4 lados + topo, com o furo do microfone, a abertura do USB-C e o furo da tecla | Topo na mesa, sem suporte |
| `base` | Fundo com a grade do falante, o anel que segura o falante e os 4 pés | Deitada, sem suporte |
| `berco` | Segura a XIAO e o amplificador no lugar | A definir |
| `tecla` | Botão do topo, de outra cor | Em pé |
