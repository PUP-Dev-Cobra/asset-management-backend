class Config(object):
  DEBUG = False
  TESTING = False

class ProductionConfig(Config):
  pass

class DevelopmentConfig(Config):
  ENV = "development"
  SQLALCHEMY_DATABASE_URI = "mssql+pymssql://<username>:<password>@<server>/<db>"
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  DEBUG = True

class TestingConfig(Config):
  TESTING = False