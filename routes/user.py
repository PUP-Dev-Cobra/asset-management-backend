from flask import Blueprint

user = Blueprint('user_route', __name__)


@user.route('/')
def index():
  return '<h1>hey</h1>'
