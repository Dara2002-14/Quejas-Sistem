@echo off
REM Script para iniciar el servidor frontend (Windows)

echo Iniciando servidor frontend...
echo Puerto: 5000
echo URL: http://127.0.0.1:5000
echo.
echo Abre tu navegador en: http://127.0.0.1:5000/index.html
echo.

cd frontend
python -m http.server 5000

