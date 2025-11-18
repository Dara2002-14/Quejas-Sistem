"""Rutas para gestión de quejas"""
import uuid
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models import Complaint, ComplaintTracker, User


complaint_bp = Blueprint('complaints', __name__, url_prefix='/api/complaints')


def is_admin(user_id):
    """Verificar si un usuario es administrador"""
    # Convertir a int si es string (JWT devuelve string)
    user_id = int(user_id) if isinstance(user_id, str) else user_id
    user = User.query.get(user_id)
    return user and user.role == 'admin'


@complaint_bp.route('/', methods=['POST'])
@jwt_required()
def create_complaint():
    """Crear una nueva queja (requiere autenticación)"""
    try:
        user_id = get_jwt_identity()
        # Convertir a int si es string (JWT devuelve string)
        user_id = int(user_id) if isinstance(user_id, str) else user_id
        
        # Verificar que el usuario existe
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'Usuario no encontrado'}), 404

        data = request.get_json() or {}
        title = data.get('title', '').strip()
        description = data.get('description', '').strip()

        # Validaciones
        if not title or not description:
            return jsonify({
                'error': 'title y description son requeridos'
            }), 400

        if len(title) < 5:
            return jsonify({
                'error': 'El título debe tener al menos 5 caracteres'
            }), 400

        if len(description) < 10:
            return jsonify({
                'error': 'La descripción debe tener al menos 10 caracteres'
            }), 400

        # Generar número único de queja
        complaint_number = str(uuid.uuid4())[:8].upper()

        # Crear queja
        complaint = Complaint(
            complaint_number=complaint_number,
            user_id=user_id,
            title=title,
            description=description
        )
        db.session.add(complaint)
        db.session.flush()  # Para obtener el ID sin commit

        # Crear registro inicial en el tracker
        track = ComplaintTracker(
            complaint_id=complaint.id,
            actor_id=user_id,
            action="created",
            note="Queja creada por el usuario"
        )
        db.session.add(track)
        db.session.commit()

        return jsonify({
            'message': 'Queja creada exitosamente',
            'complaint': complaint.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Error al crear la queja',
            'details': str(e)
        }), 500


@complaint_bp.route('/mine', methods=['GET'])
@jwt_required()
def my_complaints():
    """Obtener todas las quejas del usuario autenticado"""
    try:
        user_id = get_jwt_identity()
        # Convertir a int si es string (JWT devuelve string)
        user_id = int(user_id) if isinstance(user_id, str) else user_id
        
        # Verificar que el usuario existe
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'Usuario no encontrado'}), 404

        complaints = Complaint.query.filter_by(user_id=user_id).order_by(
            Complaint.created_at.desc()
        ).all()

        return jsonify({
            'complaints': [c.to_dict() for c in complaints],
            'count': len(complaints)
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'Error al obtener las quejas',
            'details': str(e)
        }), 500


@complaint_bp.route('/all', methods=['GET'])
@jwt_required()
def all_complaints():
    """Obtener todas las quejas (solo administradores)"""
    try:
        user_id = get_jwt_identity()
        # Convertir a int si es string (JWT devuelve string)
        user_id = int(user_id) if isinstance(user_id, str) else user_id
        
        # Verificar que el usuario existe y es admin
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'Usuario no encontrado'}), 404

        if not is_admin(user_id):
            return jsonify({
                'error': 'Acceso denegado. Solo administradores pueden ver todas las quejas'
            }), 403

        complaints = Complaint.query.order_by(
            Complaint.created_at.desc()
        ).all()

        return jsonify({
            'complaints': [c.to_dict() for c in complaints],
            'count': len(complaints)
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'Error al obtener las quejas',
            'details': str(e)
        }), 500


@complaint_bp.route('/<int:complaint_id>', methods=['GET'])
@jwt_required()
def get_complaint(complaint_id):
    """Obtener una queja específica por ID"""
    try:
        user_id = get_jwt_identity()
        # Convertir a int si es string (JWT devuelve string)
        user_id = int(user_id) if isinstance(user_id, str) else user_id
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'Usuario no encontrado'}), 404

        complaint = Complaint.query.get_or_404(complaint_id)

        # Verificar permisos: el usuario debe ser el dueño o un admin
        if complaint.user_id != user_id and not is_admin(user_id):
            return jsonify({
                'error': 'No tienes permiso para ver esta queja'
            }), 403

        return jsonify({
            'complaint': complaint.to_dict()
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'Error al obtener la queja',
            'details': str(e)
        }), 500

