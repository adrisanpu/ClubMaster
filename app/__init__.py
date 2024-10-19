from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')

    # Import and register blueprints, models, etc.
    from .routes import main, auth, events
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(events)

    return app