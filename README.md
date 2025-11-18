# Sistema de Quejas

Sistema completo de gestión de quejas con backend Flask y frontend HTML/JavaScript.

## 🚀 Inicio Rápido

### Prerrequisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Instalación

1. **Instalar dependencias del backend:**
```bash
pip install -r requirements.txt
```

2. **Inicializar la base de datos (primera vez):**
```bash
cd backend
flask db upgrade
```

### Ejecutar el Proyecto

Necesitas ejecutar **dos servidores** en terminales separadas:

#### Opción 1: Usando los scripts (Recomendado)

**Terminal 1 - Backend:**
```bash
# En macOS/Linux:
chmod +x start_backend.sh
./start_backend.sh

# En Windows:
start_backend.bat
```

**Terminal 2 - Frontend:**
```bash
# En macOS/Linux:
chmod +x start_frontend.sh
./start_frontend.sh

# En Windows:
start_frontend.bat
```

#### Opción 2: Manual

**Terminal 1 - Backend:**
```bash
cd backend
python -m flask run --host=0.0.0.0 --port=5001 --debug
```

**Terminal 2 - Frontend:**
```bash
cd frontend
python -m http.server 5000
```

### Acceder a la Aplicación

- **Frontend:** http://127.0.0.1:5000/index.html
- **Backend API:** http://127.0.0.1:5001
- **Login:** http://127.0.0.1:5000/login.html

### Estructura del Proyecto

```
Quejas-Sistem/
├── backend/           # API Flask
│   ├── run.py        # Punto de entrada
│   ├── models.py     # Modelos de base de datos
│   ├── auth_routes.py
│   └── complaint_routes.py
├── frontend/         # Interfaz web
│   ├── index.html
│   ├── login.html
│   └── js/
└── requirements.txt  # Dependencias Python
```

### Notas Importantes

- El backend corre en el **puerto 5001**
- El frontend corre en el **puerto 5000**
- Asegúrate de que ambos servidores estén corriendo simultáneamente
- El CORS está configurado para permitir comunicación entre ambos puertos

### Solución de Problemas

**Error: "Module not found"**
- Asegúrate de haber instalado las dependencias: `pip install -r requirements.txt`

**Error: "Port already in use"**
- Verifica que no haya otro proceso usando los puertos 5000 o 5001
- En macOS/Linux: `lsof -i :5001` o `lsof -i :5000`
- En Windows: `netstat -ano | findstr :5001`

**Error de CORS en el navegador**
- Verifica que el backend esté corriendo en el puerto 5001
- Revisa la consola del navegador para más detalles
