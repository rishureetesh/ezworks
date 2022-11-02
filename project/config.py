import os


# 'mysql://username:password@localhost/db_name'

class BaseConfig:
    """Base configuration"""
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_BASE_URL')
    MYSQL_DATABASE_CHARSET = 'utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_PRE_PING = True
    SECRET_KEY = 'thisissecretandsecure'



class DevelopmentConfig(BaseConfig):
    """Development configuration"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    MYSQL_DATABASE_CHARSET = 'utf8mb4'


class TestingConfig(BaseConfig):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_TEST_URL')
    MYSQL_DATABASE_CHARSET = 'utf8mb4'


class StagingConfig(BaseConfig):
    """Staging configuration"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_STAGE_URL')
    MYSQL_DATABASE_CHARSET = 'utf8mb4'


class ProductionConfig(BaseConfig):
    """Production configuration"""
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_DEPLOYMENT_URL')
    MYSQL_DATABASE_CHARSET = 'utf8mb4'

HOST = '0.0.0.0'
PORT = 5001
PATH = os.getcwd()