from flask import Blueprint

# Définir le Blueprint localement
bp = Blueprint('api', __name__)

# Ne pas importer les modules ici pour éviter les importations circulaires
# Ces importations seront faites dans create_app()
