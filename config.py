import os

class Config:
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///workshops.db'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'una_clave_secreta_fuerte'
