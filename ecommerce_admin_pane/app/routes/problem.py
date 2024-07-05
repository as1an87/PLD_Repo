from flask import Blueprint, request, jsonify
from app.models import Problem
from flask_jwt_extended import jwt_required, get_jwt_identity
bp = Blueprint('problem', __name__)
@bp.route('/problems', methods=['POST'])
@jwt_required()
def submit_problem():
    data = request.get_json()
    new_problem = Problem(description=data['description'], user_id=get_jwt_identity())
    db.session.add(new_problem)
    db.session.commit()
    return jsonify({"msg": "Problem submitted"}), 201
@bp.route('/problems', methods=['GET'])
@jwt_required()
def list_problems():
    problems = Problem.query.all()
    return jsonify([{"id": p.id, "description": p.description, "resolved": p.resolved} for p in problems]), 200
@bp.route('/problems/respond', methods=['POST'])
@jwt_required()
def respond_problem():
    current_user = get_jwt_identity()
    if not User.query.get(current_user).is_admin:
        return jsonify({"msg": "Admin access required"}), 403
    data = request.get_json()
    problem = Problem.query.get(data['problem_id'])
    if problem:
        problem.resolved = True
        db.session.commit()
        return jsonify({"msg": "Problem resolved"}), 200
    return jsonify({"msg": "Problem not found"}), 404
