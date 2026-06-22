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

Nesta seção, analisa-se a natureza do processo de busca aplicado ao Problema da Feira e como ele se diferencia dos algoritmos tradicionais de busca em caminho (pathfinding) no espaço de estados.

Abordagem de Busca Local vs. Busca em Caminho Clássica

 Os algoritmos clássicos de busca em caminho (como Busca em Largura, Busca em Profundidade, A* ou Dijkstra) exploram o espaço de estados de forma a encontrar uma sequência exata de passos (um caminho ordenado) que conecta um estado inicial bem definido a um estado objetivo. Nesses sistemas, o custo do caminho percorrido é um fator crítico e o foco está na rota.
 O Problema da Feira, conforme estruturado na atual implementação, afasta-se dessa dinâmica e adota uma abordagem de Busca Local e Melhoria Iterativa. O agente Alice altera incrementalmente a composição da sua cesta atual por meio de operadores de modificação (adicionar, remover ou substituir itens).
- Foco no Estado Final: O objetivo do algoritmo não é registrar ou otimizar o caminho (a ordem cronológica em que as frutas foram colocadas ou retiradas da sacola), mas puramente encontrar um estado de destino cuja configuração de itens resulte em um custo total o mais próximo possível do orçamento estipulado.
- Ausência de Grafo de Transição Explícito na Memória: Ao invés de expandir e armazenar uma árvore ou grafo de caminhos alternativos abertos (como faz o algoritmo A*), a busca local mantém em memória apenas o estado atual e seus candidatos gerados imediatamente na vizinhança. Isso reduz a complexidade de espaço para O(1), tornando o processo viável diante da explosão combinatória do catálogo de produtos.
 Caso o problema fosse convertido para uma busca em caminho estrita, cada nó do grafo representaria uma configuração parcial da cesta, e as arestas seriam as ações de transição. Contudo, devido ao fator de ramificação exponencial e à profundidade necessária para consumir orçamentos elevados, a busca local por melhoria iterativa se mostra uma estratégia computacionalmente mais adequada e robusta para o cenário industrial de otimização combinatória.

---

## 7. Agente Inteligente

 Explique o ciclo percepção–ação do agente, a noção de racionalidade aplicada, as decisões tomadas e o comportamento emergente observado. 

Esta seção dedica-se à caracterização e classificação taxonômica do agente implementado (Alice) com base nos conceitos fundamentais de Inteligência Artificial estabelecidos pela literatura clássica (AIMA - Russell & Norvig).

Classificação do Agente
 O agente Alice é classificado de forma proeminente como um Agente Baseado em Objetivos (Goal-Based Agent).

 A inteligência do sistema emerge do fato de que suas ações não são meras reações reflexas automáticas a estímulos imediatos. O agente possui uma descrição explícita de uma situação desejada — atingir o orçamento alvo minimizando o erro absoluto (h(s) = |orcamento - total(s)|) — e utiliza essa meta combinada com sua função heurística para avaliar e selecionar quais ações disponíveis no espaço de vizinhança devem ser executadas.

Mapeamento PEAS (Performance, Environment, Actuators, Sensors)

 Para formalizar o comportamento e o escopo operacional do sistema, a arquitetura é descrita através da matriz PEAS:
- Medida de Desempenho (Performance): A proximidade em relação ao orçamento alvo (erro de convergência igual a 0.0 para status OTIMA ou minimizado para status APROXIMADA), combinada com a eficiência computacional medida pelo número de iterações utilizadas.
- Ambiente (Environment): O mercado de compras virtual, cujas propriedades físicas irredutíveis são o catálogo de produtos e seus respectivos preços fornecidos dinamicamente pelo arquivo de entrada CSV.
- Atuadores (Actuators): As funções lógicas que executam os operadores de ação no sistema, alterando o dicionário do estado interno por meio de modificações discretas: adicionar item, remover item ou substituir item.
- Sensores (Sensors): O pipeline de leitura de dados que permite ao agente absorver e processar as percepções do ambiente, mapeando o arquivo de entrada e calculando o valor acumulado (total) da cesta corrente a cada ciclo.

Propriedades do Ambiente de Tarefa

 O ambiente no qual Alice atua possui propriedades bem delimitadas que ditam a complexidade do algoritmo:
- Totalmente Observável: O agente tem acesso completo e irrestrito a todas as informações relevantes do cenário de uma só vez através do carregamento do CSV (todos os itens e preços são conhecidos de antemão).
- Determinístico: O resultado de qualquer ação é perfeitamente previsível. Se o agente decide executar a ação de adicionar uma unidade de um item de valor conhecido, o custo final da cesta será alterado de forma exata e matemática, sem margem para ruídos ou incertezas físicas.
- Estático: O ambiente permanece imóvel e imutável enquanto o agente delibera. Os preços e a disponibilidade dos produtos no mercado não sofrem alterações dinâmicas no decorrer das iterações do laço de busca principal.
- Discreto: O espaço de estados e ações é finito e enumerável. As quantidades de itens são representadas por contadores inteiros e as iterações progridem em etapas lógicas sequenciais perfeitamente definidas.


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
