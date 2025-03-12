class Config:
    """Base configuration class.
    
    Contains default configuration settings for the application.
    All other configuration classes inherit from this class.
    """
    DEBUG = False
    TESTING = False
    SECRET_KEY = "your-default-secret-key"  # Clé secrète pour Flask
    JWT_SECRET_KEY = "your-super-secret-key"  # Clé secrète pour JWT

class DevelopmentConfig(Config):
    """Development configuration settings.
    
    Used for local development with debugging enabled.
    """
    DEBUG = True
    SECRET_KEY = "dev-secret-key"  # Remplace par une clé plus sécurisée
    JWT_SECRET_KEY = "dev-super-secret-key"  # Clé secrète pour JWT en dev

class TestingConfig(Config):
    """Testing configuration settings.
    
    Used for running tests with testing mode enabled.
    """
    TESTING = True
    SECRET_KEY = "test-secret-key"
    JWT_SECRET_KEY = "test-super-secret-key"

class ProductionConfig(Config):
    """Production configuration settings.
    
    Used for deployment in production environment.
    """
    SECRET_KEY = "prod-secret-key"
    JWT_SECRET_KEY = "prod-super-secret-key"  # Change cette clé en prod
