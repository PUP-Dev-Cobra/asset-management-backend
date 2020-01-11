from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from routes.user import user

app = Flask(__name__)
app.config.from_object('internals.config.DevelopmentConfig')
app.register_blueprint(user, url_prefix='/user')

db = SQLAlchemy(app)
