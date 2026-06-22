# Relatório Técnico
## Problema da Feira — Busca em Espaço de Estados, Agentes Inteligentes e Heurísticas

---

> **Grupo:**  The Best Of The Class
>
> **Integrantes:**  Anna Leticia do Nascimento Soares Duarte, Alice Mariana de Souza, Gustavo de Morais Lopes e Vitória Eloise de Assis Rocha
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

 Este relatório descreve a implementação e análise de um agente inteligente para o Problema da Feira, cujo objetivo é identificar uma combinação de itens de mercado cujo valor total seja igual ou o mais próximo possível de um orçamento pré-definido. O problema pertence à classe dos problemas de otimização combinatória, sendo modelado formalmente como um problema de busca em espaço de estados e resolvido por meio de um agente heurístico estocástico.
O trabalho dialoga diretamente com os fundamentos de Inteligência Artificial apresentados em Russell e Norvig (2021), em especial com os capítulos dedicados a agentes racionais, formulação de problemas de busca, busca local e heurísticas. O agente implementado, denominado Alice, opera em um ambiente totalmente observável, estático, determinístico e discreto, executando um ciclo percepção–deliberação–ação orientado pela minimização de uma função heurística de erro absoluto.
Além do interesse técnico-algorítmico, a atividade possui dimensão pedagógica ampla: permite discutir por que abordagens de IA clássica — simbólicas, heurísticas e auditáveis — continuam relevantes e, em muitos contextos práticos, preferíveis a modelos de aprendizado profundo. Questões de sustentabilidade computacional, interpretabilidade (XAI), governança algorítmica e regulamentação — incluindo o PL 2688/2025 — são discutidas ao longo do relatório à luz da implementação realizada.
Os objetivos específicos desta atividade são:
-> modelar formalmente o problema como um espaço de estados;
-> implementar um agente heurístico estocástico com melhoria iterativa;
-> analisar experimentalmente o comportamento do agente sob diferentes parâmetros;
-> discutir as relações conceituais com busca não informada, busca informada e agentes racionais;
-> refletir sobre interpretabilidade, auditabilidade e sustentabilidade da solução.


---

## 2. Modelagem Formal

 Defina formalmente: ambiente, estado, ações, espaço de estados, objetivo e heurística. Use a notação apresentada na contextualização. 

---

## 3. Representação em Grafo

 O espaço de estados do Problema da Feira é estruturado como um grafo implícito e direcionado, no qual cada nó representa um estado (configuração da cesta) e cada aresta representa a aplicação de um operador (ação do agente). O grafo é denominado implícito porque não é construído explicitamente na memória: os sucessores de um estado são gerados sob demanda durante a busca. 
 
3.1 Estrutura do Grafo:

Nó	--> Estado da cesta: mapeamento item → quantidade
Aresta	--> Aplicação de um operador (adicionar, remover, substituir)
Nó inicial	--> Cesta vazia: {Laranja:0, Banana:0, Melancia:0, Melão:0, Manga:0}
Nó objetivo -->	Qualquer estado com TOTAL = ORÇAMENTO (h(s) = 0)
Caminho -->	Sequência ordenada de ações executadas pelo agente
Peso da aresta	--> Variação de h(s) causada pela ação

3.2 Exemplo de Transições
Considerando o ambiente definido em data/feira.csv e um orçamento de R$ 5,00, a seguinte sequência ilustra transições no grafo:

Nó 0:  {Laranja:0, Banana:0, Melancia:0, Melão:0, Manga:0}  TOTAL=0,00  h=5,00

  ── adicionar(Melancia) -->
  
Nó 1:  {Laranja:0, Banana:0, Melancia:1, Melão:0, Manga:0}  TOTAL=3,00  h=2,00

  ── adicionar(Manga) -->
  
Nó 2:  {Laranja:0, Banana:0, Melancia:1, Melão:0, Manga:1}  TOTAL=3,75  h=1,25

  ── adicionar(Laranja) -->
  
Nó 3:  {Laranja:1, Banana:0, Melancia:1, Melão:0, Manga:1}  TOTAL=4,25  h=0,75

  ── adicionar(Manga) -->
  
Nó 4:  {Laranja:1, Banana:0, Melancia:1, Melão:0, Manga:2}  TOTAL=5,00  h=0,00 


O caminho acima representa uma solução ótima encontrada em 4 transições. Na prática, o agente pode percorrer caminhos muito mais longos — com avanços e retrocessos — antes de convergir para h(s) = 0, pois a seleção de ações é estocástica e nem toda transição reduz o erro.

3.3 Dimensionalidade do Espaço de Estados
Com 5 itens e quantidades potencialmente ilimitadas, o espaço de estados é tecnicamente infinito. Na prática, o orçamento impõe um limite superior para a quantidade de qualquer item: para Banana (R$ 0,05), por exemplo, o máximo possível com orçamento de R$ 20,00 é 400 unidades. Isso torna o espaço de estados finito, mas de cardinalidade muito elevada, inviabilizando abordagens exaustivas.


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

 Este trabalho apresentou a implementação e análise de um agente heurístico estocástico para o Problema da Feira, modelado formalmente como um problema de busca em espaço de estados. O agente Alice opera por melhoria iterativa guiada pela heurística h(s) = |ORÇAMENTO − TOTAL|, selecionando ações aleatoriamente e aceitando apenas as que reduzem o erro.
Os experimentos demonstraram que o agente converge consistentemente para soluções ótimas (h = 0) para orçamentos variados, com número de iterações dependente da seed e da decomposição do orçamento nos preços disponíveis. O registro estruturado da trajetória viabiliza interpretabilidade, rastreabilidade e auditabilidade — propriedades essenciais no contexto do marco regulatório de IA em discussão no Brasil.
Os principais aprendizados desta atividade foram:
a modelagem formal de um problema real como espaço de estados é o fundamento de qualquer solução algorítmica em IA;
heurísticas simples e bem escolhidas podem guiar buscas eficientes em espaços de estados de alta dimensionalidade;
a análise experimental com variação de parâmetros é indispensável para caracterizar o comportamento de agentes estocásticos;
auditabilidade e interpretabilidade não são propriedades opcionais, mas requisitos de projeto em sistemas de IA responsável;
IA clássica continua relevante e estratégica para uma ampla classe de problemas práticos.

Como extensões naturais do projeto, destacam-se a implementação de aceitação probabilística (Simulated Annealing), a comparação com algoritmos genéticos e a generalização para ambientes com restrições adicionais (e.g., limite de peso ou volume da cesta).

---

## Referências Bibliográficas

> LUGER, George F. *Artificial Intelligence: Structures and Strategies
> for Complex Problem Solving*. 6. ed. Boston: Addison-Wesley/Pearson
> Education, 2009.

> RUSSELL, Stuart J.; NORVIG, Peter. *Artificial Intelligence: A Modern
> Approach*. 4. ed. Hoboken: Pearson, 2021.
