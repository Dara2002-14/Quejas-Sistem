"""Aplicación principal Flask - Factory Pattern"""
import sys
import os

# Agregar el directorio backend al path para imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from extensions import db, migrate, jwt
from auth_routes import auth_bp
from complaint_routes import complaint_bp


def create_app(config_class=Config):
    """
    Factory function para crear la aplicación Flask.
    Permite testing y múltiples instancias.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Configurar CORS
    CORS(
        app,
        origins=app.config.get("CORS_ORIGINS", ["*"]),
        supports_credentials=app.config.get("CORS_SUPPORTS_CREDENTIALS", True),
        allow_headers=app.config.get("CORS_ALLOW_HEADERS", ["Content-Type", "Authorization"]),
        methods=app.config.get("CORS_METHODS", ["GET", "POST", "PUT", "DELETE", "OPTIONS"])
    )

    # Registrar blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(complaint_bp)

    # Ruta de salud/health check
    @app.route('/')
    def index():
        return jsonify({
            'message': 'API Sistema de Quejas',
            'status': 'running',
            'version': '1.0.0'
        })

    # Manejo de errores global
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Endpoint no encontrado'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({'error': 'Error interno del servidor'}), 500

    return app


# Instancia de la aplicación
app = create_app()


def init_db():
    """Inicializar la base de datos si no existe"""
    with app.app_context():
        # Crear todas las tablas si no existen
        db.create_all()
        print("✅ Base de datos inicializada")


if __name__ == "__main__":
    # Inicializar base de datos al iniciar
    init_db()
    print("\n🚀 Servidor iniciado en http://0.0.0.0:5001")
    print("📝 API disponible en http://127.0.0.1:5001/api\n")
    app.run(debug=True, host='0.0.0.0', port=5001)


