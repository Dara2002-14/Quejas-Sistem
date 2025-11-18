# 📋 Instrucciones para Ejecutar el Proyecto en macOS

## 🚀 Inicio Rápido

### Paso 1: Instalar Dependencias (Solo la primera vez)

```bash
pip3 install -r requirements.txt
```

### Paso 2: Inicializar Base de Datos (Solo la primera vez)

```bash
cd backend
flask db upgrade
cd ..
```

### Paso 3: Ejecutar el Proyecto

Necesitas **DOS terminales** abiertas:

#### Terminal 1 - Backend (API Flask)
```bash
./start_backend.sh
```

Deberías ver:
```
🚀 Iniciando servidor backend Flask...
📍 Puerto: 5001
🌐 URL: http://127.0.0.1:5001

 * Running on http://0.0.0.0:5001
```

#### Terminal 2 - Frontend (Interfaz Web)
```bash
./start_frontend.sh
```

Deberías ver:
```
🚀 Iniciando servidor frontend...
📍 Puerto: 5000
🌐 URL: http://127.0.0.1:5000

📝 Abre tu navegador en: http://127.0.0.1:5000/index.html
```

### Paso 4: Abrir en el Navegador

Abre tu navegador y ve a:
- **Login:** http://127.0.0.1:5000/login.html
- **Home:** http://127.0.0.1:5000/index.html

---

## 🔧 Comandos Manuales (Alternativa)

Si los scripts no funcionan, puedes ejecutar manualmente:

### Backend:
```bash
cd backend
python3 run.py
```

### Frontend:
```bash
cd frontend
python3 -m http.server 5000
```

---

## ✅ Verificar que Todo Funciona

1. **Backend funcionando:**
   - Abre: http://127.0.0.1:5001
   - Deberías ver: `{"message": "API Sistema de Quejas", "status": "running", "version": "1.0.0"}`

2. **Frontend funcionando:**
   - Abre: http://127.0.0.1:5000/index.html
   - Deberías ver la página de inicio

3. **Probar Login:**
   - Ve a: http://127.0.0.1:5000/login.html
   - Si no tienes cuenta, ve a: http://127.0.0.1:5000/register.html

---

## 🛠️ Solución de Problemas

### Error: "Permission denied"
```bash
chmod +x start_backend.sh start_frontend.sh
```

### Error: "Module not found"
```bash
pip3 install -r requirements.txt
```

### Error: "Port already in use"
```bash
# Ver qué proceso está usando el puerto
lsof -i :5001
lsof -i :5000

# Matar el proceso (reemplaza PID con el número que aparece)
kill -9 PID
```

### Error: "No module named flask"
```bash
pip3 install Flask Flask-SQLAlchemy Flask-Migrate Flask-JWT-Extended Flask-CORS python-dotenv Werkzeug
```

---

## 📝 Notas Importantes

- ✅ Mantén **ambas terminales abiertas** mientras uses la aplicación
- ✅ El backend debe estar corriendo antes de usar el frontend
- ✅ Si cierras una terminal, ese servidor se detendrá
- ✅ Para detener los servidores, presiona `Ctrl + C` en cada terminal

