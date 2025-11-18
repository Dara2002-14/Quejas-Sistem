import os
from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Configuración de la aplicación Flask"""
    
    # Base de datos
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", 
        f"sqlite:///{os.path.join(basedir, 'app.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Seguridad
    SECRET_KEY = os.getenv("SECRET_KEY", "clave-secreta-cambiar-en-produccion")
    SECRET_ADMIN_TOKEN = os.getenv("SECRET_ADMIN_TOKEN", "token-admin-cambiar")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "super-secret-jwt-key-cambiar")
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", 86400))  # 24 horas
    
    # CORS Configuration
    CORS_ORIGINS = os.getenv(
        "CORS_ORIGINS", 
        "http://localhost:3000,http://localhost:5000,http://localhost:8080,http://127.0.0.1:5000,http://127.0.0.1:3000,http://127.0.0.1:8080"
    ).split(",")
    CORS_SUPPORTS_CREDENTIALS = True
    CORS_ALLOW_HEADERS = ["Content-Type", "Authorization", "X-ADMIN-TOKEN"]
    CORS_METHODS = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
