#!/bin/sh

#
# Problema da Feira
#
# Script de execução experimental.
#
# Realiza múltiplas execuções do agente Alice
# utilizando diferentes parâmetros:
#
# - orçamento
# - limite de iterações
# - seed
#
# Objetivos pedagógicos:
#
# - observar comportamento estocástico;
# - comparar execuções;
# - analisar convergência;
# - discutir qualidade heurística;
# - introduzir experimentação computacional.
#

CSV="data/feira.csv"

echo "=================================================="
echo "Problema da Feira - Execuções Experimentais"
echo "=================================================="

echo
echo "[1]"
python3 main.py "$CSV" 20.00 50 1

echo
echo "[2]"
python3 main.py "$CSV" 20.00 500 2

echo
echo "[3]"
python3 main.py "$CSV" 20.00 1000 3

echo
echo "[4]"
python3 main.py "$CSV" 25.00 10000 4

echo
echo "[5]"
python3 main.py "$CSV" 10.00 10000 5

echo
echo "[6]"
python3 main.py "$CSV" 50.00 20000 6

echo
echo "[7]"
python3 main.py "$CSV" 7.35 15000 7

echo
echo "[8]"
python3 main.py "$CSV" 13.70 12000 8

echo
echo "[9]"
python3 main.py "$CSV" 99.99 50000 9

echo
echo "[10]"
python3 main.py "$CSV" 20.00 100000 42

echo
echo "=================================================="
echo "Fim das execuções"
echo "=================================================="
