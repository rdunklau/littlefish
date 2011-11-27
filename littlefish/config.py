from flask import Config


class LittlefishConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://littlefish@localhost/littlefish'
    SQLALCHEMY_ECHO = True
    SECRET_KEY = 'alkzjedklj'
