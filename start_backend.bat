@echo off
REM Script para iniciar el servidor backend Flask (Windows)

echo Iniciando servidor backend Flask...
echo Puerto: 5001
echo URL: http://127.0.0.1:5001
echo.

cd backend
python -m flask run --host=0.0.0.0 --port=5001 --debug

