from flask import Flask
from .models import db
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')

    # Configuring the database URI
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///events.db'  # Replace with your database URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    """# Replace these placeholders with actual RDS values:
    db_user = "admin"
    db_password = "12345678"
    db_endpoint = "discostu.c98m0cac6hdb.us-east-1.rds.amazonaws.com"
    db_name = "discostu"

    # SQLAlchemy Database URI configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{db_user}:{db_password}@{db_endpoint}:3306/{db_name}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False"""

    # Initialize the database with the app
    db.init_app(app)

    # Import and register blueprints, models, etc.
    from .routes import main, auth
    from tests.test_routes import test
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(test)

    # Create tables if they do not exist (only for development)
    with app.app_context():
        db.create_all()

    return app