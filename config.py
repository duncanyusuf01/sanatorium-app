import os

class Config:
    """
    Configuration class for the Flask application.
    Reads from environment variables or uses sensible defaults.
    """
    
    # Secret key for session management, CSRF protection, etc.
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a_super_secret_key_for_development'
    
    # Database configuration
    # Ensure you create a PostgreSQL database named 'the_sanatorium_db'
    # or update this URI to point to your database.
    # Format: postgresql://[user]:[password]@[host]:[port]/[dbname]
    DB_USER = os.environ.get('DB_USER', 'postgres')
    DB_PASS = os.environ.get('DB_PASS', '11927938') # Change this!
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_NAME = os.environ.get('DB_NAME', 'the_sanatorium_db')
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}'
        
    # Silence the SQLAlchemy deprecation warning
    SQLALCHEMY_TRACK_MODIFICATIONS = False
