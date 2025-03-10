from flask import Flask
from flask_restx import Api
from flask_jwt_extended import JWTManager
from .api.v1.users import api as users_ns
from .api.v1.amenities import api as amenities_ns
from .api.v1.places import api as places_ns
from .api.v1.reviews import api as reviews_ns
from .config import Config

# Initialiser JWTManager en dehors de la fonction pour pouvoir l'importer ailleurs
jwt = JWTManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    
    # Charger la configuration
    app.config.from_object(config_class)
    
    # Initialiser JWT
    jwt.init_app(app)
    
    api = Api(
        app, 
        version='1.0', 
        title='HBNB API', 
        description='HBNB Application API', 
        doc='/api/v1/'
    )

    # Register namespaces
    api.add_namespace(users_ns)
    api.add_namespace(amenities_ns)
    api.add_namespace(places_ns)
    api.add_namespace(reviews_ns)

    return app
