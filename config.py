import os

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get(
        'SECRET_KEY') or os.urandom(32)


class ProductionConfig(Config):
    DEBUG = False
    ASSETS_DEBUG = False
    GOOGLE_CLIENT_ID= os.environ.get('GOOGLE_OAUTH_ID')
    GOOGLE_CLIENT_SECRET=  os.environ.get('GOOGLE_OAUTH_SECRET')


class StagingConfig(Config):
    DEVELOPMENT = False
    DEBUG = False
    ASSETS_DEBUG = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    ASSETS_DEBUG = False
    GOOGLE_CLIENT_ID= os.environ.get('GOOGLE_OAUTH_ID')
    GOOGLE_CLIENT_SECRET=  os.environ.get('GOOGLE_OAUTH_SECRET')


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    ASSETS_DEBUG = True

S3_BUCKET = os.environ.get("S3_BUCKET")
S3_KEY= os.environ.get("S3_KEY")
S3_SECRET = os.environ.get("S3_SECRET")
S3_LOCATION= f'http://{S3_BUCKET}.s3.us-east-2.amazonaws.com/'
DEFAULT_IMAGE= 'default_image.jpg'
GOOGLE_CLIENT_ID= os.environ.get('GOOGLE_OAUTH_ID')
GOOGLE_CLIENT_SECRET=  os.environ.get('GOOGLE_OAUTH_SECRET')
