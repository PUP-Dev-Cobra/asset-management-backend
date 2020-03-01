from internals.app import db


class Invoices(db.Model):

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
    member_id = db.Column(
        db.Integer,
        db.ForeignKey('members.id'),
        nullable=False
    )
    loan_id = db.Column(
        db.Integer,
        db.ForeignKey('loans.id'),
        nullable=True
    )
    invoice_type = db.Column(
        db.String,
        nullable=False
    )
    amount = db.Column(
        db.Float,
        nullable=False
    )
    status = db.Column(
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
        nullable=True
    )
    updated_by_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=True
    )
