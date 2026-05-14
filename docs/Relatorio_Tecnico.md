# Relatório Técnico
## Problema da Feira — Busca em Espaço de Estados, Agentes Inteligentes e Heurísticas

---

> **Grupo:**  Nome do grupo 
>
> **Integrantes:**  Nomes dos integrantes 
>
> **Repositório:**  URL do repositório privado 
>
> **Data de entrega:** 22 de junho de 2026

---

> A contextualização teórica deste relatório — modelagem formal, relação
> com o AIMA, busca, XAI e sustentabilidade — está disponível em
> [`docs/README.md`](README.md) e deve ser utilizada como base para a redação das
> seções abaixo. O relatório deve ser autoral: não copie a contextualização,
> aplique-a à sua implementação.

---

# Sumário

- [1. Introdução](#1-introdução)
- [2. Modelagem Formal](#2-modelagem-formal)
- [3. Representação em Grafo](#3-representação-em-grafo)
- [4. Busca Não Informada](#4-busca-não-informada)
- [5. Busca Heurística](#5-busca-heurística)
- [6. Busca em Caminho](#6-busca-em-caminho)
- [7. Agente Inteligente](#7-agente-inteligente)
- [8. Resultados Experimentais](#8-resultados-experimentais)
- [9. Discussão Conceitual](#9-discussão-conceitual)
- [10. Conclusão](#10-conclusão)
- [Referências Bibliográficas](#referências-bibliográficas)

---

## 1. Introdução

 Explique o problema, os objetivos da atividade e a relação com IA. 

---

## 2. Modelagem Formal

 Defina formalmente: ambiente, estado, ações, espaço de estados, objetivo e heurística. Use a notação apresentada na contextualização. 

---

## 3. Representação em Grafo

 Explique como o problema se estrutura como grafo implícito: nós, arestas, caminhos e transições. Inclua exemplos concretos com os itens de data/feira.csv. 

---

## 4. Busca Não Informada

 Discuta BFS, DFS e a explosão combinatória do espaço de estados deste problema. Argumente por que busca exaustiva é inviável. 

---

## 5. Busca Heurística

 Explique a heurística h(s) implementada, a política de aceitação adotada e o mecanismo de melhoria iterativa. Discuta as escolhas de projeto realizadas. 

---

## 6. Busca em Caminho

 Explique como o agente registra sua trajetória, o papel dos logs e como isso contribui para interpretabilidade e auditabilidade. 

---

## 7. Agente Inteligente

 Explique o ciclo percepção–ação do agente, a noção de racionalidade aplicada, as decisões tomadas e o comportamento emergente observado. 

---

## 8. Resultados Experimentais

 Apresente os resultados obtidos com experimento.py.
 Inclua tabelas, gráficos gerados por visualizacao.py e análise dos logs. Discuta o efeito de seeds, orçamentos e limites de iterações sobre a qualidade da solução. 

---

## 9. Discussão Conceitual

 Relacione a implementação com os conceitos teóricos estudados.
 Discuta as limitações do agente, compare com outras abordagens
 de IA e reflita sobre racionalidade, heurística e emergência. 

---

## 10. Conclusão

 Sintetize os resultados, os principais aprendizados, as dificuldades encontradas e as possíveis extensões do projeto. 

---

## Referências Bibliográficas

> LUGER, George F. *Artificial Intelligence: Structures and Strategies
> for Complex Problem Solving*. 6. ed. Boston: Addison-Wesley/Pearson
> Education, 2009.

> RUSSELL, Stuart J.; NORVIG, Peter. *Artificial Intelligence: A Modern
> Approach*. 4. ed. Hoboken: Pearson, 2021.
