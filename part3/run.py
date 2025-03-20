from app import create_app
from config import DevelopmentConfig
from app.models import init_app

"""Entry point for running the Flask application.

This module creates and configures the Flask application instance using
the create_app factory function. When run directly, it starts the 
development server on localhost port 5000 with debug mode enabled.
"""

app = create_app(DevelopmentConfig)

# Initialize the database
init_app(app)

if __name__ == '__main__':
    try:
        print("Starting Flask application...")
        app.run(host='127.0.0.1', port=5000, debug=True)
    except Exception as e:
        print(f"Error starting the application: {e}")
