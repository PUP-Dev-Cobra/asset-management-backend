from flask import request, jsonify, make_response, current_app
from flask_restful import Resource, reqparse
from datetime import datetime, timedelta
from uuid import uuid4
import jwt

from internals.app import db
from internals.utils import token_required, decode_token, user_check
from models.users import Users as UserModel, users_schema, user_schema

parser = reqparse.RequestParser()
parser.add_argument('email', type=str, required=True)
parser.add_argument('password', type=str, required=True)


class User(Resource):

    @token_required
    @user_check(user_type=['admin'])
    def get(self, uuid):
        user = UserModel.query.filter_by(uuid=uuid).first()
        result = user_schema.dump(user)

        return make_response({'response': result}, 200)

    @token_required
    @user_check(user_type=['admin'])
    def post(self):
        params = request.get_json(force=True)
        decodedToken = decode_token()
        params = {
            **params,
            'password': UserModel.hashPassword(params['password']),
            'uuid': uuid4(),
            'created_at': datetime.now(),
            'created_by_id': decodedToken['id']
        }

        try:
            userParams = UserModel(**params)
            db.session.add(userParams)
            db.session.commit()

            return {'response': True}
        except:
            return make_response({'error': 'Something is wrong'}, 500)

    @token_required
    @user_check(user_type=['admin'])
    def put(self, uuid):
        params = request.get_json(force=True)
        decodedToken = decode_token()
        updateParams = {
            **params,
            'updated_at': datetime.now(),
            'updated_by_id': decodedToken['id']
        }

        if params.get('password'):
            updateParams['password'] = UserModel.hashPassword(
                params['password'])

        try:
            UserModel.query.filter_by(uuid=uuid).update(updateParams)
            db.session.commit()

            return {'response': True}
        except:
            return make_response({'error': 'Something is wrong'}, 500)

    @token_required
    @user_check(user_type=['admin'])
    def delete(self, uuid):
        decodeToken = decode_token()

        if (decodeToken.get('user_type') == 'admin'):
            try:
                UserModel.query.filter_by(uuid=uuid).delete()
                db.session.commit()

                return make_response({'response': True})
            except:
                return make_response({'error': 'Something is wrong'}, 500)

        return make_response({'error': 'permission denied'})


class List(Resource):

    @token_required
    @user_check(user_type=['admin'])
    def get(self):
        try:
            users = UserModel.query.filter_by().all()
            result = users_schema.dump(users)
            return make_response({'response': result}, 200)
        except NameError:
            return make_response({'error': 'Something is wrong'}, 500)


class Authenticate(Resource):

    def post(self):
        args = parser.parse_args()
        result = UserModel().verifyUser(args['email'], args['password'])

        if result.get('error'):
            return make_response(jsonify(result), 403)
        else:
            token = jwt.encode({
                **result,
                'exp': datetime.utcnow() + timedelta(minutes=100),
            },
                current_app.config['SECRET_KEY']
            )
            return jsonify({'token': token.decode('UTF-8')})
