class Config(object):
  DEBUG = False
  TESTING = False
  SALT = 'this is a salt'
  SECRET_KEY = 'this is a secret key'


class ProductionConfig(Config):
  pass


class DevelopmentConfig(Config):
  ENV = "development"
  SQLALCHEMY_DATABASE_URI = "mssql+pymssql://<username>:<password>@<server>/<db>"
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  DEBUG = True
  MAILGUN_API_KEY = ''
  MAILGUN_DOMAIN = ''
  BASE_EMAIL = []
  FRONT_END_DOMAIN = ''


class TestingConfig(Config):
  TESTING = False
