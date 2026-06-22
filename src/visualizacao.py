#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
visualizacao.py — Geração de gráficos para o Problema da Feira

Lê os logs gerados pelo agente e o CSV do experimento.py
e gera 4 gráficos para o relatório técnico.

Gráficos gerados:
    1. Curva de convergência de h(s) ao longo das iterações
    2. Comparação de curvas entre execuções com seeds distintas
    3. Distribuição do erro final entre execuções
    4. Taxa de soluções ótimas por configuração de parâmetros

Uso:
    python3 visualizacao.py

Dependência:
    pip install matplotlib
"""

import csv
import re
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


# ============================================================
# Configuração de caminhos
# ============================================================

DIR_LOGS    = Path(__file__).parent / "logs"
CSV_EXPERIMENTO = Path(__file__).parent / "data" / "resultados_experimento.csv"
DIR_GRAFICOS = Path(__file__).parent / "data" / "graficos"


# ============================================================
# Leitura dos logs
# ============================================================

def parsear_h_do_log(caminho):
    """
    Extrai a sequência de valores h(s) de um arquivo de log.
    Retorna uma lista de floats, um por iteração registrada.
    """
    valores_h = []
    padrao = re.compile(r"h=([\d.]+)")

    with open(caminho, encoding="utf-8") as f:
        for linha in f:
            match = padrao.search(linha)
            if match:
                valores_h.append(float(match.group(1)))

    return valores_h


def listar_logs(orcamento=None, seed=None):
    """
    Retorna lista de arquivos de log filtrados por orçamento e/ou seed.
    """
    logs = list(DIR_LOGS.glob("*.txt"))

    if orcamento is not None:
        orc_str = f"orc{str(orcamento).replace('.', '_')}"
        # Tenta com duas casas decimais também
        orc_str2 = f"orc{orcamento:.2f}".replace(".", "_")
        logs = [l for l in logs if orc_str in l.name or orc_str2 in l.name]

    if seed is not None:
        logs = [l for l in logs if f"seed{seed}__" in l.name]

    return sorted(logs)


def carregar_csv_experimento():
    """Lê o CSV de resultados do experimento."""
    dados = []
    with open(CSV_EXPERIMENTO, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            dados.append({
                "orcamento":       float(row["orcamento"]),
                "max_iter":        int(row["max_iter"]),
                "n_execucoes":     int(row["n_execucoes"]),
                "taxa_otimas_pct": float(row["taxa_otimas_pct"]),
                "erro_medio":      float(row["erro_medio"]),
                "desvio_padrao":   float(row["desvio_padrao"]),
                "iter_medio":      float(row["iter_medio"])
            })
    return dados


# ============================================================
# Gráfico 1 — Curva de convergência de h(s)
# ============================================================

def grafico_convergencia(orcamento=20.0, seed=0):
    """
    Plota h(s) ao longo das iterações para uma execução específica.
    """
    logs = listar_logs(orcamento=orcamento, seed=seed)

    if not logs:
        print(f"[Aviso] Nenhum log encontrado para orc={orcamento}, seed={seed}")
        return

    h_valores = parsear_h_do_log(logs[0])

    if not h_valores:
        print(f"[Aviso] Log sem valores de h(s): {logs[0].name}")
        return

    fig, ax = plt.subplots(figsize=(8, 4))

    ax.plot(range(1, len(h_valores) + 1), h_valores,
            color="#2196F3", linewidth=1.5, label=f"seed={seed}")

    ax.axhline(y=0, color="#E53935", linewidth=1, linestyle="--", label="objetivo h=0")

    ax.set_title(f"Convergência de h(s) — orçamento R${orcamento:.2f}", fontsize=13)
    ax.set_xlabel("Iteração")
    ax.set_ylabel("h(s) = |orçamento − total|")
    ax.legend()
    ax.grid(True, alpha=0.3)

    caminho = DIR_GRAFICOS / "convergencia.png"
    fig.tight_layout()
    fig.savefig(caminho, dpi=150)
    plt.close(fig)
    print(f"Salvo: {caminho}")


# ============================================================
# Gráfico 2 — Comparação de curvas entre seeds distintas
# ============================================================

def grafico_comparacao_seeds(orcamento=20.0, seeds=None):
    """
    Plota h(s) por iteração para múltiplos seeds no mesmo gráfico.
    """
    if seeds is None:
        seeds = [0, 1, 2, 3, 4]

    cores = ["#2196F3", "#E53935", "#4CAF50", "#FF9800", "#9C27B0"]

    fig, ax = plt.subplots(figsize=(9, 5))

    plotados = 0
    for seed, cor in zip(seeds, cores):
        logs = listar_logs(orcamento=orcamento, seed=seed)
        if not logs:
            continue

        h_valores = parsear_h_do_log(logs[0])
        if not h_valores:
            continue

        ax.plot(range(1, len(h_valores) + 1), h_valores,
                color=cor, linewidth=1.4, alpha=0.85, label=f"seed={seed}")
        plotados += 1

    if plotados == 0:
        print(f"[Aviso] Nenhum log encontrado para orc={orcamento}")
        return

    ax.axhline(y=0, color="black", linewidth=1, linestyle="--", label="objetivo h=0")

    ax.set_title(f"Comparação entre seeds — orçamento R${orcamento:.2f}", fontsize=13)
    ax.set_xlabel("Iteração")
    ax.set_ylabel("h(s) = |orçamento − total|")
    ax.legend(loc="upper right")
    ax.grid(True, alpha=0.3)

    caminho = DIR_GRAFICOS / "comparacao_seeds.png"
    fig.tight_layout()
    fig.savefig(caminho, dpi=150)
    plt.close(fig)
    print(f"Salvo: {caminho}")


# ============================================================
# Gráfico 3 — Distribuição do erro final por orçamento
# ============================================================

def grafico_distribuicao_erro(max_iter=100):
    """
    Plota o erro médio por orçamento para um dado max_iter.
    Barras de erro mostram o desvio padrão.
    """
    dados = carregar_csv_experimento()
    filtrados = [d for d in dados if d["max_iter"] == max_iter]

    if not filtrados:
        print(f"[Aviso] Sem dados para max_iter={max_iter}")
        return

    orcamentos  = [d["orcamento"] for d in filtrados]
    erros       = [d["erro_medio"] for d in filtrados]
    desvios     = [d["desvio_padrao"] for d in filtrados]
    rotulos     = [f"R${o:.0f}" for o in orcamentos]

    fig, ax = plt.subplots(figsize=(9, 4))

    barras = ax.bar(rotulos, erros, color="#42A5F5", edgecolor="white",
                    linewidth=0.8, yerr=desvios, capsize=4,
                    error_kw={"ecolor": "#1565C0", "linewidth": 1.5})

    ax.set_title(f"Erro médio final por orçamento (max_iter={max_iter})", fontsize=13)
    ax.set_xlabel("Orçamento-alvo")
    ax.set_ylabel("Erro médio | desvio padrão")
    ax.yaxis.set_major_formatter(ticker.FormatStrFormatter("%.3f"))
    ax.grid(True, axis="y", alpha=0.3)

    for barra, erro in zip(barras, erros):
        if erro > 0:
            ax.text(barra.get_x() + barra.get_width() / 2,
                    barra.get_height() + max(desvios) * 0.05,
                    f"{erro:.3f}", ha="center", va="bottom", fontsize=8)

    caminho = DIR_GRAFICOS / "distribuicao_erro.png"
    fig.tight_layout()
    fig.savefig(caminho, dpi=150)
    plt.close(fig)
    print(f"Salvo: {caminho}")


# ============================================================
# Gráfico 4 — Taxa de soluções ótimas por configuração
# ============================================================

def grafico_taxa_otimas():
    """
    Plota a taxa de soluções ótimas (%) por orçamento,
    com uma linha por valor de max_iter.
    """
    dados = carregar_csv_experimento()

    max_iters   = sorted(set(d["max_iter"] for d in dados))
    orcamentos  = sorted(set(d["orcamento"] for d in dados))
    rotulos     = [f"R${o:.0f}" for o in orcamentos]

    cores = {100: "#E53935", 1000: "#FF9800", 10000: "#43A047"}

    fig, ax = plt.subplots(figsize=(9, 4))

    for mi in max_iters:
        taxas = []
        for orc in orcamentos:
            entrada = next(
                (d for d in dados if d["orcamento"] == orc and d["max_iter"] == mi),
                None
            )
            taxas.append(entrada["taxa_otimas_pct"] if entrada else 0)

        cor = cores.get(mi, "#999999")
        ax.plot(rotulos, taxas, marker="o", linewidth=2,
                color=cor, label=f"max_iter={mi}")

    ax.set_title("Taxa de soluções ótimas por orçamento e max_iter", fontsize=13)
    ax.set_xlabel("Orçamento-alvo")
    ax.set_ylabel("Soluções ótimas (%)")
    ax.set_ylim(-5, 110)
    ax.axhline(y=100, color="gray", linewidth=0.8, linestyle="--")
    ax.legend()
    ax.grid(True, alpha=0.3)

    caminho = DIR_GRAFICOS / "taxa_otimas.png"
    fig.tight_layout()
    fig.savefig(caminho, dpi=150)
    plt.close(fig)
    print(f"Salvo: {caminho}")


# ============================================================
# Main
# ============================================================

def main():
    DIR_GRAFICOS.mkdir(parents=True, exist_ok=True)

    print("Gerando gráficos...\n")

    grafico_convergencia(orcamento=20.0, seed=0)
    grafico_comparacao_seeds(orcamento=20.0, seeds=[0, 1, 2, 3, 4])
    grafico_distribuicao_erro(max_iter=100)
    grafico_taxa_otimas()

    print(f"\nTodos os gráficos salvos em: {DIR_GRAFICOS}")


if __name__ == "__main__":
    main()
