from flask import current_app, make_response
from internals.app import db
from marshmallow import Schema, fields
from schemas.users import UserSchema
from internals.app import create_app
from datetime import datetime
from internals.mailgun import send_simple_message
from pathlib import Path

import hashlib, binascii, os


class Users(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
        unique=True
    )
    uuid = db.Column(
        db.String(100),
        nullable=False,
        unique=True
    )
    name = db.Column(
        db.String,
        nullable=False,
        default='Generic Name'
    )
    email = db.Column(
        db.String(100),
        nullable=False,
        unique=True
    )
    password = db.Column(db.String, nullable=False)
    user_type = db.Column(
        db.String,
        nullable=False
    )
    member_id = db.Column(
        db.Integer,
        db.ForeignKey('members.id'),
        nullable=True
    )
    status = db.Column(
        db.String(10),
        nullable=False
    )
    reset_password_hash = db.Column(
        db.String,
        nullable=True
    )
    created_at = db.Column(
        db.DATETIME,
        nullable=False
    )
    updated_at = db.Column(
        db.DATETIME,
        nullable=True
    )
    created_by_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=True
    )
    updated_by_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=True
    )

    def createForgotPassword(self, email):
        app = current_app
        salt = app.config['SALT']
        domain = app.config['FRONT_END_DOMAIN']
        time = datetime.now()

        try:
            user = self.query.filter_by(email=email).first()
            if user is not None:
                hashString = "%s%s" % (salt, time.utcnow().isoformat())
                hashReset = hashlib.md5(hashString.encode('utf-8'))
                hashUrl = "%sreset-password/%s" % (domain, hashReset.hexdigest())

                self\
                    .query\
                    .filter_by(email=email)\
                    .update({'reset_password_hash': hashReset.hexdigest()})

                send_simple_message(
                    subject='Reset Password for %s' % (user.name),
                    text=Path('./templates/email.template.html')
                    .read_text()
                    .replace("{{name}}", user.name)
                    .replace("{{url}}", hashUrl)
                )

                db.session.commit()
            return {"response": "User reset cerdentials are sent"}
        except:
            return {"response": "User reset cerdentials are sent"}

    def resetPassword(self, resetHash, password):
        try:
            user = self.query.filter_by(reset_password_hash=resetHash).first()

            if user is not None:
                passwordHash = Users.hashPassword(password)
                self\
                    .query\
                    .filter_by(id=user.id)\
                    .update({
                        'password': passwordHash,
                        'reset_password_hash': None
                    })
                db.session.commit()
            return
        except:
            raise Exception('Something is wrong')

    def hashPassword(textPassword):
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
        pwdhash = hashlib.pbkdf2_hmac(
            'sha512',
            textPassword.encode('utf-8'),
            salt,
            10000
        )
        pwdhash = binascii.hexlify(pwdhash)
        return (salt + pwdhash).decode('ascii')

    def verifyPassword(storedPassword, providedPassword):
        salt = storedPassword[:64]
        storedPassword = storedPassword[64:]
        pwdHash = hashlib.pbkdf2_hmac(
            'sha512',
            providedPassword.encode('UTF-8'),
            salt.encode('ascii'),
            10000
        )
        pwdHash = binascii.hexlify(pwdHash).decode('ascii')
        return pwdHash == storedPassword

    def verifyUser(self, email, password):
        user = self.query.filter_by(email=email).first()
        error = {'error': 'Invalid username and password'}

        if user is None:
            return error
        elif user.status == 'disable':
            return {'error': 'User is disabled'}
        else:
            storedPassword = user.password
            isMatch = Users.verifyPassword(storedPassword, password)

            if isMatch:
                jsonToken = {
                    'isMatch': isMatch,
                    'id': user.id,
                    'email': user.email,
                    'uuid': user.uuid,
                    'user_type': user.user_type
                }
                if (user.user_type == 'member'):
                    jsonToken['member_id'] = user.memberInfo.uuid

                return jsonToken
            else:
                return error

        return isMatch


user_schema = UserSchema()
users_schema = UserSchema(many=True)
