#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Problema da Feira

Este módulo representa o ambiente no qual
o agente Alice irá atuar.

O ambiente contém:

- itens disponíveis;
- preços;
- orçamento alvo.

O agente recebe percepções do ambiente
e executa ações buscando minimizar o erro
em relação ao orçamento desejado.
"""

import sys
import csv
import os
from pathlib import Path
from datetime import datetime

from solucao import agente_alice


DEFAULT_MAX_ITER = 10000

LOG_DIR = Path(__file__).parent / "logs"


# ============================================================
# Geração e gravação do log
# ============================================================

def nome_log(agente, csv_path, orcamento, seed):
    """
    Gera um nome semântico para o arquivo de log.

    Formato:
        <agente>__<csv>__orc<orcamento>__seed<seed>__<timestamp>.txt

    Exemplo:
        alice__feira__orc20.00__seed42__20260614_153022.txt
    """

    base_csv = Path(csv_path).stem
    seed_str = str(seed) if seed is not None else "none"
    orc_str = f"{orcamento:.2f}".replace(".", "_")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    return (
        f"{agente}"
        f"__{base_csv}"
        f"__orc{orc_str}"
        f"__seed{seed_str}"
        f"__{timestamp}.txt"
    )


def gravar_log(caminho, resultado, ambiente, csv_path, orcamento, seed, max_iter):
    """
    Grava o arquivo de log da execução do agente.

    O log contém:

    - cabeçalho com parâmetros da execução;
    - trajetória de ações registradas pelo agente;
    - rodapé com resultado final.
    """

    itens = ambiente["itens"]

    with open(caminho, "w", encoding="utf-8") as f:

        # Cabeçalho

        f.write("=" * 60 + "\n")
        f.write("PROBLEMA DA FEIRA — LOG DE EXECUÇÃO\n")
        f.write("=" * 60 + "\n")
        f.write(f"AGENTE    : alice\n")
        f.write(f"CSV       : {csv_path}\n")
        f.write(f"ORCAMENTO : {orcamento:.2f}\n")
        f.write(f"MAX_ITER  : {max_iter}\n")
        f.write(f"SEED      : {seed}\n")
        f.write(f"TIMESTAMP : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("\n")

        # Itens disponíveis no ambiente

        f.write("ITENS DISPONÍVEIS:\n")
        for item, preco in itens.items():
            f.write(f"  {item}: R$ {preco:.2f}\n")
        f.write("\n")

        # Trajetória

        f.write("TRAJETÓRIA:\n")

        if resultado.entradas_log:
            for entrada in resultado.entradas_log:
                f.write(f"  {entrada}\n")
        else:
            f.write("  (nenhuma ação registrada)\n")

        f.write("\n")

        # Resultado final

        f.write("=" * 60 + "\n")
        f.write("RESULTADO FINAL\n")
        f.write("=" * 60 + "\n")

        for item, quantidade in resultado.estado.items():
            f.write(f"  {item}: {quantidade}\n")

        f.write(f"TOTAL     : {resultado.total:.2f}\n")
        f.write(f"ERRO      : {resultado.erro:.2f}\n")
        f.write(f"ITERACOES : {resultado.iteracoes}\n")
        f.write(f"STATUS    : {resultado.status}\n")


# ============================================================
# Leitura do ambiente
# ============================================================

def carregar_itens(csv_path):

    itens = {}

    with open(csv_path, newline='', encoding='utf-8') as csvfile:

        reader = csv.DictReader(csvfile)

        for row in reader:

            item = row["item"]
            preco = float(row["preco"])

            itens[item] = preco

    return itens


# ============================================================
# Processamento de argumentos
# ============================================================

def parse_args():

    if len(sys.argv) < 3:

        print(
            f"Uso: {sys.argv[0]} "
            "<itens.csv> <orcamento> "
            "[max_iter] [seed]"
        )

        sys.exit(1)

    csv_path = sys.argv[1]
    orcamento = float(sys.argv[2])

    max_iter = DEFAULT_MAX_ITER
    seed = None

    if len(sys.argv) >= 4:
        max_iter = int(sys.argv[3])

    if len(sys.argv) >= 5:
        seed = int(sys.argv[4])

    return csv_path, orcamento, max_iter, seed


# ============================================================
# Impressão da saída
# ============================================================

def imprimir_saida(resultado):

    for item, quantidade in resultado.estado.items():
        print(f"{item}: {quantidade}")

    print(f"TOTAL: {resultado.total:.2f}")
    print(f"ERRO: {resultado.erro:.2f}")
    print(f"ITERACOES: {resultado.iteracoes}")
    print(f"STATUS: {resultado.status}")
    print(f"LOG: {resultado.log}")


# ============================================================
# Main
# ============================================================

def main():

    csv_path, orcamento, max_iter, seed = parse_args()

    #
    # Construção explícita do ambiente
    #

    ambiente = {
        "itens": carregar_itens(csv_path),
        "orcamento": orcamento
    }

    resultado = agente_alice(
        ambiente=ambiente,
        max_iter=max_iter,
        seed=seed
    )

    #
    # Gravação do log
    #

    LOG_DIR.mkdir(parents=True, exist_ok=True)

    arquivo_log = LOG_DIR / nome_log(
        agente="alice",
        csv_path=csv_path,
        orcamento=orcamento,
        seed=seed
    )

    gravar_log(
        caminho=arquivo_log,
        resultado=resultado,
        ambiente=ambiente,
        csv_path=csv_path,
        orcamento=orcamento,
        seed=seed,
        max_iter=max_iter
    )

    #
    # Resultado com caminho do log preenchido
    #

    resultado = resultado._replace(log=str(arquivo_log))

    imprimir_saida(resultado)


if __name__ == "__main__":
    main()
