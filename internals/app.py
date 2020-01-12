from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from internals.config import DevelopmentConfig
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    db.init_app(app)
    migrate.init_app(app, db)
    from models import users, options, members, loans

    from routes.user import user
    app.register_blueprint(user, url_prefix='/user')
    return app
