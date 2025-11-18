#!/bin/bash

# Script para iniciar el servidor backend Flask (macOS)

echo "🚀 Iniciando servidor backend Flask..."
echo "📍 Puerto: 5001"
echo "🌐 URL: http://127.0.0.1:5001"
echo ""

# Cambiar al directorio backend desde la raíz del proyecto
cd "$(dirname "$0")/backend" || exit

# Ejecutar Flask directamente con run.py
# Usar PYTHONPATH para asegurar que los imports funcionen
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
python3 run.py

