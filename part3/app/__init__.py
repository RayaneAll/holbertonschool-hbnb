from flask import Flask
from flask_restx import Api
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy  # Ajout de l'import SQLAlchemy
from config import Config

# Initialiser JWTManager en dehors de la fonction pour pouvoir l'importer ailleurs
jwt = JWTManager()
db = SQLAlchemy()  # Initialisation de SQLAlchemy

def create_app(config_class=Config):
    app = Flask(__name__)
    
    # Charger la configuration
    app.config.from_object(config_class)
    
    # Initialiser JWT
    jwt.init_app(app)
    
    # Initialiser SQLAlchemy
    db.init_app(app)  # Ajout de cette ligne
    
    api = Api(
        app,
        version='1.0',
        title='HBNB API',
        description='HBNB Application API',
        doc='/api/v1/'
    )
    
    # Importer les namespaces ici, à l'intérieur de la fonction
    from .api.v1.users import api as users_ns
    from .api.v1.amenities import api as amenities_ns
    from .api.v1.places import api as places_ns
    from .api.v1.reviews import api as reviews_ns
    from .api.v1.auth import api as auth_ns  # Nouveau namespace pour l'authentification
    
    # Register namespaces
    api.add_namespace(users_ns)
    api.add_namespace(amenities_ns)
    api.add_namespace(places_ns)
    api.add_namespace(reviews_ns)
    api.add_namespace(auth_ns)  # Enregistrement du namespace d'authentification
    
    return app
