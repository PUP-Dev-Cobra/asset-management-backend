from internals.app import db
from schemas.disbursments import DisbursmentsSchema


class Disbursments(db.Model):

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
    loan_id = db.Column(
        db.Integer,
        db.ForeignKey('loans.id'),
        nullable=False
    )
    check_voucher = db.Column(
        db.String,
        nullable=False
    )
    check_number = db.Column(
        db.String,
        nullable=False
    )
    signatory = db.Column(
        db.String,
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
    status = db.Column(
        db.String,
        nullable=False
    )
    issue_date = db.Column(
        db.Date,
        nullable=False
    )
    encashment = db.relationship(
        'Encashments',
        lazy=True,
        backref='disbursmentInfo'
    )


def disbursment_schema(many=False, **kwargs):
    return DisbursmentsSchema(many=many, **kwargs)
