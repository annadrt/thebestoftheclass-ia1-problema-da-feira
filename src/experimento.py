#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
experimento.py — Análise experimental quantitativa do agente Alice

Executa o agente repetidamente com diferentes combinações de
parâmetros (orçamento, limite de iterações, seed) e exporta
uma linha por execução individual para src/data/resultados_experimento.csv.

Uso:
    python3 experimento.py
"""

import csv
import sys
import math
from pathlib import Path
from solucao import agente_alice
from main import carregar_itens


# ============================================================
# Configuração dos experimentos
# ============================================================

CSV_ITENS = Path(__file__).parent / "data" / "feira.csv"
CSV_SAIDA = Path(__file__).parent / "data" / "resultados_experimento.csv"

ORCAMENTOS = [10.00, 15.00, 20.00, 25.00, 30.00, 50.00]
MAX_ITERS  = [100, 1000, 10000]
SEEDS      = list(range(10))


# ============================================================
# Execução dos experimentos
# ============================================================

def executar_experimentos(itens):
    """
    Para cada combinação (orcamento, max_iter, seed), executa o agente
    e registra os resultados individuais.
    """
    registros = []
    total = len(ORCAMENTOS) * len(MAX_ITERS) * len(SEEDS)
    executados = 0

    for orcamento in ORCAMENTOS:
        for max_iter in MAX_ITERS:
            for seed in SEEDS:

                ambiente = {"itens": itens, "orcamento": orcamento}
                resultado = agente_alice(
                    ambiente=ambiente,
                    max_iter=max_iter,
                    seed=seed
                )

                registros.append({
                    "orcamento": orcamento,
                    "max_iter":  max_iter,
                    "seed":      seed,
                    "erro":      resultado.erro,
                    "iteracoes": resultado.iteracoes,
                    "status":    resultado.status
                })

                executados += 1
                print(
                    f"[{executados}/{total}] "
                    f"orc={orcamento:.2f} "
                    f"max_iter={max_iter} "
                    f"seed={seed} "
                    f"→ erro={resultado.erro:.2f} "
                    f"iter={resultado.iteracoes} "
                    f"status={resultado.status}"
                )

    return registros


# ============================================================
# Agregação de métricas
# ============================================================

def desvio_padrao(valores):
    """Desvio padrão populacional."""
    n = len(valores)
    if n == 0:
        return 0.0
    media = sum(valores) / n
    return math.sqrt(sum((v - media) ** 2 for v in valores) / n)


def agregar(registros):
    """
    Agrega resultados por (orcamento, max_iter), calculando:
        - taxa de soluções ótimas (%)
        - erro médio, mínimo, máximo e desvio padrão
        - média de iterações
    """
    grupos = {}
    for r in registros:
        chave = (r["orcamento"], r["max_iter"])
        if chave not in grupos:
            grupos[chave] = []
        grupos[chave].append(r)

    agregados = []
    for (orcamento, max_iter), grupo in sorted(grupos.items()):
        erros     = [r["erro"] for r in grupo]
        iteracoes = [r["iteracoes"] for r in grupo]
        otimas    = sum(1 for r in grupo if r["status"] == "OTIMA")

        agregados.append({
            "orcamento":       orcamento,
            "max_iter":        max_iter,
            "n_execucoes":     len(grupo),
            "taxa_otimas_pct": round(100 * otimas / len(grupo), 1),
            "erro_medio":      round(sum(erros) / len(erros), 4),
            "erro_min":        round(min(erros), 4),
            "erro_max":        round(max(erros), 4),
            "desvio_padrao":   round(desvio_padrao(erros), 4),
            "iter_medio":      round(sum(iteracoes) / len(iteracoes), 1)
        })

    return agregados


# ============================================================
# Exportação para CSV
# ============================================================

def exportar_csv(registros, caminho):
    """Exporta execuções individuais — uma linha por (orcamento, max_iter, seed)."""
    campos = ["orcamento", "max_iter", "seed", "erro", "iteracoes", "status"]
    caminho.parent.mkdir(parents=True, exist_ok=True)
    with open(caminho, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        writer.writerows(registros)
    print(f"\nResultados exportados para: {caminho}")


# ============================================================
# Main
# ============================================================

def main():
    if not CSV_ITENS.exists():
        print(f"Erro: arquivo não encontrado: {CSV_ITENS}")
        sys.exit(1)

    itens = carregar_itens(CSV_ITENS)

    print("Iniciando experimentos...\n")
    registros = executar_experimentos(itens)

    exportar_csv(registros, CSV_SAIDA)

    print("\nAgregando métricas...")
    agregados = agregar(registros)

    print("\nResumo:")
    print(
        f"{'Orçamento':>10} {'max_iter':>10} {'% Ótimas':>10}"
        f" {'Erro médio':>12} {'Erro mín':>10} {'Erro máx':>10}"
        f" {'DP erro':>10} {'Iter médio':>12}"
    )
    print("-" * 96)
    for r in agregados:
        print(
            f"{r['orcamento']:>10.2f} "
            f"{r['max_iter']:>10} "
            f"{r['taxa_otimas_pct']:>9.1f}% "
            f"{r['erro_medio']:>12.4f} "
            f"{r['erro_min']:>10.4f} "
            f"{r['erro_max']:>10.4f} "
            f"{r['desvio_padrao']:>10.4f} "
            f"{r['iter_medio']:>12.1f}"
        )


if __name__ == "__main__":
    main()
