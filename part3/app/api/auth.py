from flask import request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token
from app.models.user import User
from app.api import bp
from app.services.auth_service import verify_password

@bp.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"error": "Missing email or password"}), 400
    
    user = User.query.filter_by(email=data['email']).first()
    
    if not user or not verify_password(data['password'], user.password_hash):
        return jsonify({"error": "Invalid email or password"}), 401
    
    # Créer les tokens
    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))
    
    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user_id": str(user.id)
    }), 200
