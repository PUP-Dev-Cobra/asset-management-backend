from internals.app import db
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
        storedPassword = user.password
        isMatch = Users.verifyPassword(storedPassword, password)
        return isMatch
