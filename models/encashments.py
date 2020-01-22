from internals.app import db

from schemas.encashments import EncashmentSchema


class Encashments(db.Model):

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
    disbursment_id = db.Column(
        db.Integer,
        db.ForeignKey('disbursments.id'),
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


def encashment_schema(many=False, **kwargs):
    return EncashmentSchema(many=many, **kwargs)
