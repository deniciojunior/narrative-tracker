#!/bin/bash
set -e

export PYTHONUTF8=1   # necessario no Windows para evitar erro de encoding

echo "=== NARRATIVE TRACKER ==="
echo ""
echo "Passo 1: Coletando artigos do GDELT..."
uv run src/collector.py

echo ""
echo "Passo 2: Analisando com Claude Haiku..."
uv run src/analyzer.py

echo ""
echo "Passo 3: Calculando scores de divergencia..."
uv run src/scorer.py

echo ""
echo "Passo 4: Iniciando dashboard..."
echo "Acesse: http://localhost:5000"
echo ""
echo "Para coleta continua em background:"
echo "  PYTHONUNBUFFERED=1 uv run src/scheduler.py &"
echo ""
uv run src/app.py
