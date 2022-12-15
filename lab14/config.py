import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    DEVELOPMENT = False
    JWT_SECRET_KEY = 'super-secret'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'thesecretkey132'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True


class DevConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    WTF_CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or \
                              'sqlite:///' + os.path.join(basedir, 'site.db')


class TestConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

    HASH_ROUNDS = 1

class ProdConfig(Config):
    WTF_CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or \
                              'sqlite:///' + os.path.join(basedir, 'site.db')


config = {
    'dev': DevConfig,
    'prod': ProdConfig,
    'default': DevConfig,
    'test': TestConfig,
}
