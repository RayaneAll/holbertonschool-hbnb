from flask import Flask
from flask_restx import Api
from flask_jwt_extended import JWTManager  # Import du JWTManager
from .api.v1.users import api as users_ns
from .api.v1.amenities import api as amenities_ns
from .api.v1.places import api as places_ns
from .api.v1.reviews import api as reviews_ns

jwt = JWTManager()  # Création de l'instance JWT

def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_class)  # Charger la configuration

    # Ajout de la clé secrète pour JWT (Assurez-vous que DevelopmentConfig la définit)
    app.config["JWT_SECRET_KEY"] = "super-secret-key"  # À remplacer par une vraie clé sécurisée

    jwt.init_app(app)  # Initialiser JWT avec l'application Flask

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
