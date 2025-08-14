import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'mysecretkey123456'
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:56789@localhost/event_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

