from flask import Blueprint, request, jsonify
from app.models import Company
from flask_jwt_extended import jwt_required, get_jwt_identity
bp = Blueprint('company', __name__)
@bp.route('/companies', methods=['GET'])
@jwt_required()
def list_companies():
    companies = Company.query.all()
    return jsonify([c.name for c in companies]), 200
@bp.route('/companies/approve', methods=['POST'])
@jwt_required()
def approve_company():
    current_user = get_jwt_identity()
    if not User.query.get(current_user).is_admin:
        return jsonify({"msg": "Admin access required"}), 403
    data = request.get_json()
    company = Company.query.get(data['company_id'])
    if company:
        company.approved = True
        db.session.commit()
        return jsonify({"msg": "Company approved"}), 200
    return jsonify({"msg": "Company not found"}), 404
