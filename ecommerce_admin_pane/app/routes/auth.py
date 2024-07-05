from flask import Blueprint, request, jsonify
from app.models import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
bp = Blueprint('auth', __name__)
@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    new_user = User(username=data['username'], password_hash=data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"msg": "User registered"}), 201
@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and user.password_hash == data['password']:
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    return jsonify({"msg": "Bad username or password"}), 401
@bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh_token():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    return jsonify(access_token=access_token), 200
