from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .extensions import db
from .models import Complaint, ComplaintTracker, User
import uuid

complaint_bp = Blueprint('complaints', __name__, url_prefix='/api/complaints')


# Crear una queja (usuario autenticado)
@complaint_bp.route('/', methods=['POST'])
@jwt_required()
def create_complaint():
    user_id = get_jwt_identity()  # viene desde el token

    data = request.get_json() or {}
    title = data.get('title')
    description = data.get('description')

    if not title or not description:
        return jsonify({'error': 'title y description son requeridos'}), 400

    complaint_number = str(uuid.uuid4())[:8]  # número único

    complaint = Complaint(
        complaint_number=complaint_number,
        user_id=user_id,
        title=title,
        description=description
    )
    db.session.add(complaint)
    db.session.commit()

    # tracker inicial
    track = ComplaintTracker(
        complaint_id=complaint.id,
        actor_id=user_id,
        action="created",
        note="Queja creada por el usuario"
    )
    db.session.add(track)
    db.session.commit()

    return jsonify({
        'message': 'Queja creada',
        'complaint': complaint.to_dict()
    }), 201


# Ver mis quejas (usuario autenticado)
@complaint_bp.route('/mine', methods=['GET'])
@jwt_required()
def my_complaints():
    user_id = get_jwt_identity()
    complaints = Complaint.query.filter_by(user_id=user_id).all()

    return jsonify({
        'complaints': [c.to_dict() for c in complaints]
    }), 200


# Solo admin puede ver TODAS las quejas
@complaint_bp.route('/all', methods=['GET'])
@jwt_required()
def all_complaints():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if user.role != "admin":
        return jsonify({'error': 'Solo admins pueden ver todas las quejas'}), 403

    complaints = Complaint.query.all()
    return jsonify({
        'complaints': [c.to_dict() for c in complaints]
    }), 200

