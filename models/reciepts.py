from internals.app import db


class Reciepts(db.Model):

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
    reciept_type = db.Column(
        db.String,
        default='loan_payment'
    )
    loan_id = db.Column(
        db.Integer,
        db.ForeignKey('loans.id'),
        nullable=False,
        default=0
    )
    loan_payment_term = db.Column(
        db.Integer,
        nullable=True
    )
    or_number = db.Column(
        db.String,
        nullable=False
    )
    amount = db.Column(
        db.Float,
        nullable=False
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
        nullable=False
    )
    updated_by_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=True
    )
