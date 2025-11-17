from flask import Blueprint, request, jsonify, current_app
from .extensions import db
from .models import User
import os

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'error': 'username, email y password son obligatorios'}), 400

    if User.query.filter((User.username==username) | (User.email==email)).first():
        return jsonify({'error': 'usuario o email ya existen'}), 400

    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'Usuario creado', 'user': user.to_dict()}), 201


from flask_jwt_extended import create_access_token

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'username y password requeridos'}), 400

    user = User.query.filter(
        (User.username == username) | (User.email == username)
    ).first()

    if not user or not user.check_password(password):
        return jsonify({'error': 'credenciales inválidas'}), 401

    token = create_access_token(identity=str(user.id))  # <-- FIX AQUÍ

    return jsonify({
        'message': 'Login exitoso',
        'token': token,
        'user': user.to_dict()
    }), 200




@auth_bp.route('/create-admin', methods=['POST'])
def create_admin():
    token = request.headers.get('X-ADMIN-TOKEN')
    if token != os.getenv('SECRET_ADMIN_TOKEN'):
        return jsonify({'error': 'Token admin inválido'}), 403

    data = request.get_json() or {}
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'error': 'username, email y password son obligatorios'}), 400

    if User.query.filter((User.username==username) | (User.email==email)).first():
        return jsonify({'error': 'usuario o email ya existen'}), 400

    admin = User(username=username, email=email, role='admin')
    admin.set_password(password)
    db.session.add(admin)
    db.session.commit()
    return jsonify({'message': 'Administrador creado', 'admin': admin.to_dict()}), 201
