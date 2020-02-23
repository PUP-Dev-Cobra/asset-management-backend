from flask import request, jsonify, make_response, current_app
from flask_restful import Resource, reqparse
from datetime import datetime, timedelta
from uuid import uuid4
import jwt

from internals.app import db
from internals.utils import token_required, decode_token, user_check
from models.users import Users as UserModel, users_schema, user_schema
from models.members import Members as MemberModel

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
            userEmail = UserModel\
                .query\
                .filter_by(
                    email=params.get('email')
                )\
                .first()

            if userEmail is None:
                userParams = UserModel(**params)
                db.session.add(userParams)
                db.session.commit()

                return {'response': userParams.uuid}
            return make_response({'error': 'Email is already used'}, 500)
        except NameError:
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

        del updateParams['created_at']

        if params.get('password'):
            updateParams['password'] = UserModel\
                .hashPassword(params['password'])

        try:
            isEmailUsed = UserModel.query.filter(
                UserModel.uuid != uuid
            ).filter(
                UserModel.email == params.get('email')
            ).first()
            if isEmailUsed is None:
                UserModel.query.filter_by(uuid=uuid).update(updateParams)
                db.session.commit()

                return {'response': True}
            return make_response({'error': 'Email already used'}, 500)
        except NameError:
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
        decodeToken = decode_token()
        try:
            users = UserModel\
                .query\
                .filter(UserModel.id != decodeToken['id'])\
                .order_by(
                    UserModel.status.asc(),
                    UserModel.updated_at.desc(),
                    UserModel.created_at.desc()
                )\
                .all()
            result = users_schema.dump(users)
            return make_response({'response': result}, 200)
        except NameError:
            return make_response({'error': 'Something is wrong'}, 500)


class Authenticate(Resource):

    def post(self):
        args = parser.parse_args()
        try:
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
        except NameError:
            return make_response({'error': 'Something is wrong'}, 500)


class CreatePasswordResetHash(Resource):

    def post(self):
        args = request.get_json()
        try:
            result = UserModel().createForgotPassword(email=args['email'])
            return result
        except NameError as e:
            print(e)
            return make_response({'error': 'Something is wrong'}, 500)


class ForgotPasswordReset(Resource):

    def post(self, hash):
        args = request.get_json()
        try:
            UserModel()\
                .resetPassword(resetHash=hash, password=args['password'])
            return {'response': 'Password is reset'}
        except:
            make_response({'response': 'Soemthing is wrong'}, 500)
