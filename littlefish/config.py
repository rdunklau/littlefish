"""Global config"""
from flask import Config


class LittlefishConfig(Config):
    """Global config as class attributes"""
    SQLALCHEMY_DATABASE_URI = 'postgresql://littlefish@/littlefish'
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_NATIVE_UNICODE = True
    SECRET_KEY = 'alkzjedklj'
    WTF_CSRF_CHECK_DEFAULT = False
    WTF_CSRF_ENABLED = False
