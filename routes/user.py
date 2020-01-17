from flask import request
from flask_restful import Resource, reqparse

from models.users import Users as UserModel

parser = reqparse.RequestParser()
parser.add_argument('email', type=str, required=True)
parser.add_argument('password', type=str, required=True)


class User(Resource):

  def get(self):
    return {'hello': 'world'}


class List(Resource):

  def get(self):
    return {'hello': 'userlist'}


class Authenticate(Resource):

  def post(self):
    args = parser.parse_args()
    result = UserModel().verifyUser(args['email'], args['password'])
    return {'output': result}
