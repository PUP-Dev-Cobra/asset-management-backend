from flask import request, jsonify, make_response, current_app
from functools import wraps, partial
import jwt


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return make_response(jsonify({'error': 'Token is missing'}), 403)
        try:
            jwt.decode(token, current_app.config['SECRET_KEY'])
        except:
            return make_response(jsonify({'error': 'Token is invalid'}), 403)

        return f(*args, **kwargs)
    return decorated


def decode_token():
    return jwt.decode(
        request.headers.get('Authorization'),
        current_app.config['SECRET_KEY']
    )


def user_check(*args, **kwargs):
    def argDecroated(f):
        @wraps(f)
        def decorated(*args2, **kwargs2):
            decodeToken = decode_token()
            user_type = decodeToken.get('user_type')
            check_types = kwargs.get('user_type')
            if user_type in check_types:
                return f(*args2, **kwargs2)
            return make_response({'error': 'permission error'}, 403)
        return decorated

    return argDecroated
