from flask import Config


class LittlefishConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://littlefish@localhost:5432/littlefish'
    SQLALCHEMY_ECHO = True
    SECRET_KEY = 'alkzjedklj'
    
