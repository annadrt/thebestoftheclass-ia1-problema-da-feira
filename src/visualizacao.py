#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Problema da Feira — Visualização

Este módulo gera gráficos a partir de:

- arquivos de log individuais gerados pelo agente;
- arquivo CSV gerado pelo experimento.py.

Gráficos esperados:

- curva de convergência de h(s) ao longo das iterações;
- comparação de curvas entre execuções com seeds distintas;
- distribuição do erro final entre execuções de um experimento;
- taxa de soluções ótimas por configuração de parâmetros.

Uso:

    python3 visualizacao.py

Saída:

    Arquivos PNG salvos em data/graficos/.

Dependências:

    matplotlib — instalar com:
        pip install -r requirements.txt
"""

