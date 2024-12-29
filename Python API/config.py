import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///trail_mgmt.db'  # Using SQLite for simplicity
    SQLALCHEMY_TRACK_MODIFICATIONS = False
