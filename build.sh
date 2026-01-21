#!/bin/bash
set -e

echo "📦 Instalando dependências..."
pip install --no-cache-dir -r requirements.txt

echo "🎯 Treinando modelo com dados atualizados..."
python src/train_13_14.py

echo "🚀 Iniciando API..."
uvicorn api.main:app --host 0.0.0.0 --port 10000