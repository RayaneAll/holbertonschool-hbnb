import os
from datetime import timedelta

class Config:
    """Base configuration class.
    
    Contains default configuration settings for the application.
    All other configuration classes inherit from this class.
    """
    DEBUG = False
    TESTING = False
    
    # Configuration JWT
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'dev-secret-key')  # À changer en production
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
    # Configuration SQLAlchemy de base
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    """Development configuration settings.
    
    Used for local development with debugging enabled.
    """
    DEBUG = True
    # Base de données SQLite pour le développement
    SQLALCHEMY_DATABASE_URI = 'sqlite:///development.db'

class TestingConfig(Config):
    """Testing configuration settings.
    
    Used for running tests with testing mode enabled.
    """
    TESTING = True
    # Base de données SQLite en mémoire pour les tests
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

class ProductionConfig(Config):
    """Production configuration settings.
    
    Used for deployment in production environment.
    """
    # En production, utilisez une variable d'environnement pour l'URI de la base de données
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///production.db')
