from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token, create_refresh_token
from app.models.user import User
from app.services.auth_service import verify_password

api = Namespace('auth', description='Authentication operations')

login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

token_response = api.model('TokenResponse', {
    'access_token': fields.String(description='JWT access token'),
    'refresh_token': fields.String(description='JWT refresh token'),
    'user_id': fields.String(description='User ID'),
    'is_admin': fields.Boolean(description='Admin status')
})

@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    @api.marshal_with(token_response, code=200)
    @api.response(400, 'Missing email or password')
    @api.response(401, 'Invalid email or password')
    def post(self):
        """Authenticate user and return JWT token"""
        data = api.payload
        
        if not data or not data.get('email') or not data.get('password'):
            api.abort(400, "Missing email or password")
        
        user = User.query.filter_by(email=data['email']).first()
        
        if not user or not verify_password(data['password'], user.password_hash):
            api.abort(401, "Invalid email or password")
        
        # Ajouter le champ is_admin dans les claims du token
        additional_claims = {
            "is_admin": user.is_admin
        }
        
        # Créer les tokens avec les claims supplémentaires
        access_token = create_access_token(
            identity=str(user.id),
            additional_claims=additional_claims
        )
        refresh_token = create_refresh_token(
            identity=str(user.id),
            additional_claims=additional_claims
        )
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user_id": str(user.id),
            "is_admin": user.is_admin
        }
