import os

# Base configuration class (default settings for all environments)
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_secret_key')  # Default secret key if not set in environment
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///default.db')  # Default SQLite database
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable Flask-SQLAlchemy modification tracking to save resources


# Development environment configuration
class DevelopmentConfig(Config):
    DEBUG = True  # Enable debug mode
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URL', 'sqlite:///dev.db')  # Development database


# Testing environment configuration
class TestingConfig(Config):
    TESTING = True  # Enable testing mode
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL', 'sqlite:///test.db')  # Testing database
    WTF_CSRF_ENABLED = False  # Disable CSRF for testing forms


# Production environment configuration
class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///prod.db')  # Production database
    # Other production-specific configurations go here (e.g., security settings)


# Dictionary to easily retrieve configuration classes based on the environment
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig  # Default to development if not specified
}