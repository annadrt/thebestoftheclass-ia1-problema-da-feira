#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
solucao.py — Implementação do Agente Alice

O agente utiliza busca local com melhoria iterativa
para encontrar uma cesta cujo total se aproxime ao
máximo do orçamento-alvo, minimizando h(s) = |orçamento - total|.
"""

import random
from collections import namedtuple


# Estrutura de retorno do agente
Resultado = namedtuple(
    "Resultado",
    ["estado", "total", "erro", "iteracoes", "status", "entradas_log", "log"]
)


# ============================================================
# Funções auxiliares
# ============================================================

def calcular_total(estado, precos):
    """Calcula o custo total da cesta."""
    return sum(qtd * precos[item] for item, qtd in estado.items())


def h(estado, precos, orcamento):
    """
    Função heurística: erro absoluto entre orçamento e total da cesta.
    h(s) = |orcamento - total(s)|
    Quanto menor, melhor. h(s) = 0 indica solução ótima.
    """
    return abs(orcamento - calcular_total(estado, precos))


# ============================================================
# Operadores de ação
# ============================================================

def gerar_vizinho(estado, itens, rng):
    """
    Seleciona e aplica um operador aleatório válido:
        - adicionar: incrementa quantidade de um item
        - remover:   decrementa quantidade de um item (se > 0)
        - substituir: remove uma unidade de um item, adiciona de outro

    Retorna o novo estado e uma descrição da ação para o log.
    """
    lista = list(itens.keys())
    removiveis = [item for item in lista if estado[item] > 0]

    # Define quais ações são possíveis no estado atual
    acoes_possiveis = ["adicionar"]
    if removiveis:
        acoes_possiveis.append("remover")
        if len(lista) > 1:
            acoes_possiveis.append("substituir")

    acao = rng.choice(acoes_possiveis)
    novo_estado = dict(estado)

    if acao == "adicionar":
        item = rng.choice(lista)
        novo_estado[item] += 1
        descricao = f"adicionar {item}"

    elif acao == "remover":
        item = rng.choice(removiveis)
        novo_estado[item] -= 1
        descricao = f"remover {item}"

    else:  # substituir
        item_a = rng.choice(removiveis)
        candidatos_b = [i for i in lista if i != item_a]
        item_b = rng.choice(candidatos_b)
        novo_estado[item_a] -= 1
        novo_estado[item_b] += 1
        descricao = f"substituir {item_a} -> {item_b}"

    return novo_estado, descricao


# ============================================================
# Política de aceitação
# ============================================================

def aceitar(h_atual, h_novo):
    """
    Aceita o novo estado apenas se ele for estritamente melhor.
    Política gulosa (hill climbing).
    """
    return h_novo < h_atual


# ============================================================
# Agente Alice
# ============================================================

def agente_alice(ambiente, max_iter=10000, seed=None):
    """
    Agente que busca minimizar h(s) por melhoria iterativa.

    Parâmetros
    ----------
    ambiente : dict
        Dicionário com chaves "itens" (dict item->preco) e "orcamento" (float).
    max_iter : int
        Número máximo de iterações permitidas.
    seed : int ou None
        Semente para reprodutibilidade.

    Retorno
    -------
    Resultado : namedtuple
        Estado final, total, erro, iterações, status, log e entradas_log.
    """

    rng = random.Random(seed)

    itens = ambiente["itens"]
    orcamento = ambiente["orcamento"]

    # Estado inicial: cesta vazia
    estado_atual = {item: 0 for item in itens}
    h_atual = h(estado_atual, itens, orcamento)

    # Registra o melhor estado encontrado ao longo da busca
    melhor_estado = dict(estado_atual)
    melhor_h = h_atual

    entradas_log = []
    iteracoes = 0

    for iteracao in range(1, max_iter + 1):

        # Critério de parada: solução ótima encontrada
        if h_atual == 0:
            break

        iteracoes = iteracao

        # Gera um estado vizinho por operador aleatório
        estado_novo, descricao = gerar_vizinho(estado_atual, itens, rng)
        h_novo = h(estado_novo, itens, orcamento)
        total_novo = calcular_total(estado_novo, itens)

        # Registra a ação no log
        entradas_log.append(
            f"[{iteracao}] {descricao} | "
            f"TOTAL={total_novo:.2f} | ERRO={h_novo:.2f}"
        )

        # Aplica política de aceitação
        if aceitar(h_atual, h_novo):
            estado_atual = estado_novo
            h_atual = h_novo

            # Atualiza melhor solução global
            if h_atual < melhor_h:
                melhor_estado = dict(estado_atual)
                melhor_h = h_atual

    # Define status final
    status = "OTIMA" if melhor_h == 0 else "APROXIMADA"
    total_final = calcular_total(melhor_estado, itens)

    return Resultado(
        estado=melhor_estado,
        total=round(total_final, 2),
        erro=round(melhor_h, 2),
        iteracoes=iteracoes,
        status=status,
        log="",
        entradas_log=entradas_log
    )
