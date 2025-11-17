from flask import Flask
from .config import Config
from .extensions import db, migrate, jwt
from .auth_routes import auth_bp
from .complaint_routes import complaint_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)  # Inicializa JWT

    # Registrar blueprints
    app.register_blueprint(auth_bp, url_prefix="/api")
    app.register_blueprint(complaint_bp, url_prefix="/api")


    @app.route('/')
    def index():
        return {'message': 'API sistema_quejas corriendo'}

    return app

# Ejecutar servidor
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)


