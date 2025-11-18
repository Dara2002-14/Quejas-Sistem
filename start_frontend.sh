#!/bin/bash

# Script para iniciar el servidor frontend (macOS)

echo "🚀 Iniciando servidor frontend..."
echo "📍 Puerto: 8080"
echo "🌐 URL: http://127.0.0.1:8080"
echo ""
echo "📝 Abre tu navegador en: http://127.0.0.1:8080/index.html"
echo ""

# Cambiar al directorio frontend
cd "$(dirname "$0")/frontend" || exit

# Ejecutar servidor HTTP simple en puerto 8080
python3 -m http.server 8080

