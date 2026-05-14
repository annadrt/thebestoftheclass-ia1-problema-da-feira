# Guia de Implementação — `src/`

Este documento contém as orientações técnicas para implementação dos módulos
[`solucao.py`](solucao.py), [`experimento.py`](experimento.py) e [`visualizacao.py`](visualizacao.py).

---

# Sumário

- [1. Estrutura do Diretório](#1-estrutura-do-diretório)
- [2. Arquivos Fornecidos](#2-arquivos-fornecidos)
- [3. O Que Deve Ser Implementado](#3-o-que-deve-ser-implementado)
  - [3.1 `solucao.py` — comportamento do agente](#31-soluçãopy--comportamento-do-agente)
  - [3.2 `experimento.py` — análise experimental](#32-experimentopy--análise-experimental)
  - [3.3 `visualizacao.py` — geração de gráficos](#33-visualizacaopy--geração-de-gráficos)
- [4. Ciclo do Agente](#4-ciclo-do-agente)
- [5. Execução](#5-execução)
- [6. Saída Esperada](#6-saída-esperada)
- [7. Logs e Rastreamento](#7-logs-e-rastreamento)
- [8. Execuções Experimentais](#8-execuções-experimentais)

---

# 1. Estrutura do Diretório

```text
src/
├── data/
│   ├── feira.csv                    ← ambiente: itens e preços
│   └── resultados_experimento.csv   ← gerado por experimento.py
├── logs/                            ← gerado automaticamente por main.py
│   └── .gitkeep
├── main.py                          ← pipeline de execução (não modificar)
├── solucao.py                       ← agente Alice (a implementar)
├── experimento.py                   ← análise experimental (a implementar)
├── visualizacao.py                  ← geração de gráficos (a implementar)
├── requirements.txt                 ← dependências do projeto (a manter)
├── run.sh                           ← execuções experimentais
└── README.md                        ← este arquivo
```

---

# 2. Arquivos Fornecidos

## `main.py`

Contém a infraestrutura já implementada:

* leitura do ambiente via [`data/feira.csv`](data/feira.csv);
* parsing do CSV;
* estrutura do agente (`agente_alice()`);
* estrutura do estado (cesta);
* logging automático de ações e trajetória em `logs/`;
* formatação da saída;
* pipeline completo de execução.

> Não modifique `main.py`.

## [`data/feira.csv`](data/feira.csv)

Define o ambiente do agente: lista de itens e preços disponíveis.

Formato:

```csv
item,preco
Laranja,0.50
Banana,0.05
Melancia,3.00
Melão,2.50
Manga,0.75
```

O arquivo pode ser substituído por outro CSV com o mesmo formato para
experimentos com ambientes distintos.

## `run.sh`

Script de execuções experimentais automatizadas com diferentes orçamentos,
limites de iterações e seeds. Pode ser editado para incluir novos experimentos.

## requirements.txt

Lista de dependências externas do projeto. Atualizar sempre que uma nova
biblioteca for adicionada:

```bash
pip install -r requirements.txt
```

---

# 3. O Que Deve Ser Implementado

---

## 3.1 `solucao.py` — comportamento do agente

O estudante deverá implementar dentro do loop de busca de `agente_alice()`:

| Componente | Descrição |
|---|---|
| Cálculo do total | soma ponderada dos itens na cesta |
| Função heurística `h(s)` | `h(s) = \|ORCAMENTO - TOTAL\|` |
| Operador: adicionar item | incrementa a quantidade de um item |
| Operador: remover item | decrementa a quantidade de um item |
| Operador: substituir item | troca um item por outro |
| Geração de candidatos | seleciona aleatoriamente um operador e um item |
| Política de aceitação | aceita candidato se reduz o erro heurístico |
| Melhoria iterativa | repete o ciclo até atingir erro zero ou o limite de iterações |
| Registro de trajetória | acumula entradas em `entradas_log` a cada ação |

### Heurística

A heurística sugerida é o erro absoluto em relação ao orçamento:

$$
h(s) = |ORCAMENTO - TOTAL|
$$

O agente deve preferir estados com menor valor de `h(s)`.

### Política de aceitação

A política mínima esperada é:

```text
aceitar candidato se h(candidato) < h(estado_atual)
```

Extensões opcionais para análise e discussão:

* aceitação com tolerância (aceitar empates);
* aceitação probabilística estilo simulated annealing.

---

## 3.2 experimento.py — análise experimental

Script que executa o agente repetidamente com diferentes combinações de
parâmetros e coleta métricas quantitativas para o relatório técnico.

O módulo deverá:

* importar `agente_alice` de [`solucao.py`](solucao.py) e `carregar_itens`de [`main.py`](main.py);
* executar o agente para múltiplas combinações de orçamento, `max_iter` e seed;
* calcular por experimento: taxa de soluções ótimas, erro médio, desvio
  padrão, erro mínimo, erro máximo e média de iterações;
* imprimir tabela de resumo no terminal;
* exportar todas as execuções individuais para `data/resultados_experimento.csv`.

O CSV exportado alimenta diretamente o [`visualizacao.py`](visualizacao.py) e a seção de
Resultados Experimentais do relatório técnico.

---

## 3.3 visualizacao.py — geração de gráficos

Script que lê os arquivos de log gerados pelo agente e o CSV produzido pelo
[`experimento.py`](experimento.py) e gera gráficos em PNG para o relatório técnico.

O módulo deverá gerar:

| Gráfico | Fonte de dados | Saída |
|---|---|---|
| Curva de convergência de `h(s)` | arquivo de log | `data/graficos/` |
| Comparação de curvas entre seeds | múltiplos logs | `data/graficos/` |
| Histograma do erro final | `resultados_experimento.csv` | `data/graficos/` |
| Taxa de soluções ótimas por experimento | `resultados_experimento.csv` | `data/graficos/` |

> **Dependência:** requer `matplotlib`. Instalar com:
>
> ```bash
> pip install -r requirements.txt
> ```

---

# 4. Ciclo do Agente

Uma interação em [`solucao.py`](solucao.py) corresponde a um ciclo completo:

```text
1. perceber()       → lê o estado atual da cesta
2. gerar candidato  → escolhe aleatoriamente um operador e um item
3. executar ação    → aplica o operador ao estado
4. avaliar h(s)     → calcula o erro do novo estado
5. decidir          → aceita ou rejeita o candidato
6. registrar        → acumula entrada em entradas_log
```

O número máximo de iterações define o orçamento computacional do agente.

---

# 5. Execução

A partir do diretório `src/`:

### Execução simples

```bash
python3 main.py data/feira.csv 20.00
```

### Execução com limite de iterações e seed

```bash
python3 main.py data/feira.csv 20.00 10000 42
```

Parâmetros:

| Parâmetro | Descrição | Padrão |
|---|---|---|
| `data/feira.csv` | caminho para o arquivo de itens | obrigatório |
| `20.00` | orçamento alvo | obrigatório |
| `10000` | número máximo de iterações | opcional |
| `42` | seed do gerador aleatório | opcional |

---

# 6. Saída Esperada

```text
Laranja: 3
Banana: 10
Melancia: 3
Melão: 2
Manga: 2
TOTAL: 20.00
ERRO: 0.00
ITERACOES: 612
STATUS: OTIMA
LOG: logs/alice__feira__orc20_00__seed42__20260614_153022.txt
```

Campos:

| Campo | Descrição |
|---|---|
| `TOTAL` | valor total da cesta encontrada |
| `ERRO` | distância ao orçamento (`h(s)` final) |
| `ITERACOES` | número de ciclos executados |
| `STATUS` | `OTIMA` se erro = 0, `APROXIMADA` caso contrário |
| `LOG` | caminho do arquivo de log gerado |

---

# 7. Logs e Rastreamento

O agente registra automaticamente cada ação e transição de estado:

```text
[12] adicionar Melancia | TOTAL=12.00 | ERRO=8.00
[13] adicionar Manga    | TOTAL=12.75 | ERRO=7.25
[14] remover Laranja    | TOTAL=12.25 | ERRO=7.75
```

Os logs permitem:

* reconstruir a trajetória completa do agente;
* auditar cada decisão tomada;
* analisar a evolução da heurística ao longo da busca;
* comparar execuções com diferentes seeds.

Os logs são lidos por [`visualizacao.py`](visualizacao.py) para geração das curvas de convergência
e são a base para a discussão de XAI e auditabilidade no relatório técnico e
no questionário conceitual.

---

# 8. Execuções Experimentais

Para execuções experimentais predefinidas:

```bash
./run.sh
```

Para análise quantitativa estruturada:

```bash
python3 experimento.py
```

Para geração de gráficos a partir dos logs e do CSV experimental:

```bash
python3 visualizacao.py
```

Os resultados, logs e gráficos gerados devem ser analisados e apresentados
na seção de **Resultados Experimentais** do Relatório Técnico
[`/docs/Relatorio_Tecnico.md`](../docs/Relatorio_Tecnico.md).
