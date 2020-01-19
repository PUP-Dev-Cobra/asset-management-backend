from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from internals.config import DevelopmentConfig
from flask_migrate import Migrate
from flask_cors import CORS
from flask_restful import Api

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    api = Api(app)
    CORS(app)

    db.init_app(app)
    migrate.init_app(app, db)
    from models import users, options, members, loans

    from routes import user, option
    api.add_resource(user.User, '/user', '/user/<string:uuid>')
    api.add_resource(user.List, '/user/list')
    api.add_resource(option.Options, '/options')
    api.add_resource(user.Authenticate, '/authenticate')

    return app
