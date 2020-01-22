from marshmallow import Schema, fields

from internals.app import db
from models.loans import Loans
from models.beneficiaries import Beneficiaries
from models.shares import MemberShares
from schemas.members import MemberSchema


class Members(db.Model):

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
    nickname = db.Column(
        db.String,
        nullable=False
    )
    dob = db.Column(
        db.Date,
        nullable=False
    )
    age = db.Column(
        db.Integer,
        nullable=False
    )
    gender = db.Column(
        db.String, nullable=False
    )
    civil_status = db.Column(
        db.String,
        nullable=False
    )
    address = db.Column(
        db.String,
        nullable=False
    )
    source_of_income = db.Column(
        db.String,
        nullable=False
    )
    spouse_name = db.Column(
        db.String,
        nullable=True
    )
    monthly_income = db.Column(
        db.String,
        nullable=False
    )
    religion = db.Column(
        db.String,
        nullable=False
    )
    recommended_by = db.Column(
        db.Integer,
        db.ForeignKey('members.id'),
        nullable=True
    )
    contact_no = db.Column(
        db.String,
        nullable=False
    )
    tin_oca = db.Column(
        db.String,
        nullable=True
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
    loans = db.relationship(
        Loans,
        lazy=True,
        backref='member_info',
        foreign_keys=[Loans.member_id]
    )
    beneficiaries = db.relationship(
        Beneficiaries,
        lazy=True,
        backref='principal',
        foreign_keys=[Beneficiaries.member_id]
    )
    shares = db.relationship(
        MemberShares,
        lazy=True,
        backref='shares',
        foreign_keys=[MemberShares.member_id]
    )


def member_schema(many=False, **kwargs):
    return MemberSchema(many=many, **kwargs)
