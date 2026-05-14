# Contextualização Teórica

---

# Sumário

- [Parte I — Contextualização Teórica](#parte-i--contextualização-teórica)
  - [O Problema](#o-problema)
  - [Modelagem Formal](#modelagem-formal)
  - [Relação com o AIMA](#relação-com-o-aima)
  - [Busca Não Informada](#busca-não-informada)
  - [Busca Informada e Heurísticas](#busca-informada-e-heurísticas)
  - [Busca em Caminho](#busca-em-caminho)
  - [XAI e Auditabilidade](#xai-e-auditabilidade)
  - [Sustentabilidade Computacional e IA](#sustentabilidade-computacional-e-ia)
  - [Relações Conceituais](#relações-conceituais)

---

# Parte I — Contextualização Teórica

Esta seção apresenta o embasamento teórico da atividade. Ela serve de apoio para a implementação, para o relatório técnico e para a preparação das respostas do questionário e do seminário.

O relatório técnico deve ser desenvolvido no arquivo [`Relatorio_Tecnico.md`](Relatorio_Tecnico.md).


---

## O Problema

Alice possui um orçamento para realizar compras em uma feira. Os itens disponíveis e seus preços são definidos por um arquivo CSV. O objetivo do agente é encontrar uma combinação de itens cujo valor total seja igual ou o mais próximo possível do orçamento informado.

Formalmente:

$$
TOTAL \approx ORCAMENTO
$$

Heurística sugerida:

$$
h(s) = |ORCAMENTO - TOTAL|
$$

---

## Modelagem Formal

### Ambiente

O ambiente contém itens disponíveis, preços e orçamento alvo. Suas propriedades são:

* discreto;
* totalmente observável;
* estático;
* determinístico;
* finito.

O comportamento do agente é estocástico.

### Estado

Um estado representa a configuração atual da cesta:

```text
{
    "Laranja": 3,
    "Banana": 10,
    "Melancia": 1
}
```

### Ações

O agente pode executar:

* adicionar item;
* remover item;
* substituir item.

Cada ação representa uma transição no espaço de estados.

### Espaço de Estados

O problema deve ser interpretado como um grafo implícito:

* nós → estados;
* arestas → ações;
* caminho → sequência de ações.

---

## Relação com o AIMA

A atividade foi estruturada para dialogar com conceitos de:

> RUSSELL, Stuart J.; NORVIG, Peter. *Artificial Intelligence: A Modern Approach*. 4. ed. Hoboken: Pearson, 2021.


| Conceito | Implementação |
|---|---|
| ambiente | CSV + orçamento |
| percepção | função `perceber()` |
| agente | `agente_alice()` |
| estado | cesta atual |
| ação | adicionar/remover/substituir |
| espaço de estados | conjunto de configurações |
| heurística | erro absoluto |
| objetivo | erro = 0 |
| racionalidade | minimizar erro |
| busca local | melhoria iterativa |
| busca em caminho | histórico de ações |
| exploração estocástica | operadores aleatórios |

---

## Busca Não Informada

O exercício permite discutir BFS, DFS, explosão combinatória e a inviabilidade de busca exaustiva em espaços de estados grandes.

---

## Busca Informada e Heurísticas

A atividade introduz heurísticas como mecanismo de avaliação de estados, permitindo otimização local por melhoria iterativa e exploração guiada do espaço de busca.

---

## Busca em Caminho

O agente registra ações executadas, estados percorridos e trajetória de busca. Isso permite interpretabilidade, rastreabilidade e auditoria do comportamento do agente.

---

## XAI e Auditabilidade

A estrutura do projeto favorece interpretabilidade, transparência, rastreabilidade e auditabilidade algorítmica. Os logs permitem reconstruir:

```text
estado -> ação -> novo estado
```

aproximando o exercício de discussões sobre XAI, governança algorítmica, IA responsável e regulamentação — inclusive o PL 2688/2025 e o futuro marco regulatório brasileiro de IA.

---

## Sustentabilidade Computacional e IA

O exercício foi propositalmente estruturado com IA clássica, busca heurística, representação simbólica e métodos estocásticos simples. Isso permite discutir criticamente por que nem todo problema exige modelos fundacionais, por que heurísticas clássicas continuam relevantes e por que soluções auditáveis e eficientes continuam estratégicas.

---

## Relações Conceituais

Embora o problema aparente ser simples, sua estrutura possui relação direta com:

* problema do robô aspirador;
* busca em largura (BFS) e em profundidade (DFS);
* problema das oito rainhas;
* hill climbing;
* simulated annealing;
* algoritmos genéticos;
* agentes baseados em objetivo;
* otimização heurística.

---




