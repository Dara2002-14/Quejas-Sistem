"""Rutas de autenticación"""
import os
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from extensions import db
from models import User


auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


def validate_email(email):
    """Validación básica de email"""
    if not email or '@' not in email:
        return False
    return True


@auth_bp.route('/register', methods=['POST'])
def register():
    """Registrar un nuevo usuario"""
    try:
        data = request.get_json() or {}
        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()

        # Validaciones
        if not username or not email or not password:
            return jsonify({
                'error': 'username, email y password son obligatorios'
            }), 400

        if len(username) < 3:
            return jsonify({
                'error': 'El username debe tener al menos 3 caracteres'
            }), 400

        if len(password) < 6:
            return jsonify({
                'error': 'La contraseña debe tener al menos 6 caracteres'
            }), 400

        if not validate_email(email):
            return jsonify({
                'error': 'Email inválido'
            }), 400

        # Verificar si el usuario ya existe
        existing_user = User.query.filter(
            (User.username == username) | (User.email == email)
        ).first()

        if existing_user:
            return jsonify({
                'error': 'Usuario o email ya existen'
            }), 400

        # Crear usuario
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        return jsonify({
            'message': 'Usuario creado exitosamente',
            'user': user.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Error al crear usuario',
            'details': str(e)
        }), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """Iniciar sesión y obtener token JWT"""
    try:
        data = request.get_json() or {}
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()

        if not username or not password:
            return jsonify({
                'error': 'Username y password son requeridos'
            }), 400

        # Buscar usuario por username o email
        user = User.query.filter(
            (User.username == username) | (User.email == username)
        ).first()

        if not user or not user.check_password(password):
            return jsonify({
                'error': 'Credenciales inválidas'
            }), 401

        # Crear token JWT
        token = create_access_token(identity=str(user.id))

        return jsonify({
            'message': 'Login exitoso',
            'token': token,
            'user': user.to_dict()
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'Error al iniciar sesión',
            'details': str(e)
        }), 500


@auth_bp.route('/create-admin', methods=['POST'])
def create_admin():
    """Crear un administrador (requiere token de admin)"""
    try:
        # Verificar token de admin
        token = request.headers.get('X-ADMIN-TOKEN')
        secret_token = os.getenv('SECRET_ADMIN_TOKEN')

        if not token or token != secret_token:
            return jsonify({
                'error': 'Token admin inválido o faltante'
            }), 403

        data = request.get_json() or {}
        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()

        # Validaciones
        if not username or not email or not password:
            return jsonify({
                'error': 'username, email y password son obligatorios'
            }), 400

        if len(username) < 3:
            return jsonify({
                'error': 'El username debe tener al menos 3 caracteres'
            }), 400

        if len(password) < 6:
            return jsonify({
                'error': 'La contraseña debe tener al menos 6 caracteres'
            }), 400

        if not validate_email(email):
            return jsonify({
                'error': 'Email inválido'
            }), 400

        # Verificar si el usuario ya existe
        existing_user = User.query.filter(
            (User.username == username) | (User.email == email)
        ).first()

        if existing_user:
            return jsonify({
                'error': 'Usuario o email ya existen'
            }), 400

        # Crear administrador
        admin = User(username=username, email=email, role='admin')
        admin.set_password(password)
        db.session.add(admin)
        db.session.commit()

        return jsonify({
            'message': 'Administrador creado exitosamente',
            'admin': admin.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Error al crear administrador',
            'details': str(e)
        }), 500
