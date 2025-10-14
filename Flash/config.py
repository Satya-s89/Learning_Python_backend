import os 
from decouple import config

class Config:
    SECRET_KEY = config('SECRET_KEY', default='dev-secret-key')
    SQLALCHEMY_DATABASE_URI = config('DATABASE_URL', default='sqlite:///users.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = config('SECRET_KEY', default='dev-secret-key')