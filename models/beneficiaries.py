from marshmallow import Schema, fields

from internals.app import db
from schemas.beneficiaries import BeneficiariesSchema


class Beneficiaries(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
        unique=True
    )
    member_id = db.Column(
        db.Integer,
        db.ForeignKey('members.id'),
        nullable=False
    )
    first_name = db.Column(
        db.String,
        nullable=False
    )
    last_name = db.Column(
        db.String,
        nullable=False
    )
    middle_name = db.Column(
        db.String,
        nullable=True
    )
    dob = db.Column(
        db.Date,
        nullable=False
    )
    relationship = db.Column(
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


beneficiarie_schema = BeneficiariesSchema()
beneficiaries_schema = BeneficiariesSchema(many=True)
