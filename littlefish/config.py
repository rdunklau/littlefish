"""Global config"""
from flask import Config


class LittlefishConfig(Config):
    """Global config as class attributes"""
    SQLALCHEMY_DATABASE_URI = 'postgresql://littlefish@:6432/littlefish'
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_NATIVE_UNICODE = True
    SQLALCHEMY_ENGINE_OPTIONS = {'connect_args':  {"application_name":"littlefish"}}
    SECRET_KEY = 'alkzjedklj'
    WTF_CSRF_CHECK_DEFAULT = False
    WTF_CSRF_ENABLED = False
