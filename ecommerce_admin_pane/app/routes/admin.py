from flask import Blueprint, request, jsonify
from app import db
from app.models import User
from flask_jwt_extended import jwt_required, get_jwt_identity
bp = Blueprint('admin', __name__, url_prefix='/admin')
@bp.route('/users', methods=['POST'])
@jwt_required()
def create_admin():
    current_user = get_jwt_identity()
    if not User.query.get(current_user).is_admin:
        return jsonify({"msg": "Admin access required"}), 403
    data = request.get_json()
    new_user = User(username=data['username'], password_hash=data['password'], is_admin=True)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"msg": "Admin user created"}), 201
@bp.route('/users', methods=['GET'])
@jwt_required()
def list_admins():
    current_user = get_jwt_identity()
    if not User.query.get(current_user).is_admin:
        return jsonify({"msg": "Admin access required"}), 403
    users = User.query.filter_by(is_admin=True).all()
    return jsonify([u.username for u in users]), 200
