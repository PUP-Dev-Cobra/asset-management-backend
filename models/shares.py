from internals.app import db
from marshmallow import Schema, fields


class MemberShares(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True,
        unique=True,
        autoincrement=True
    )
    member_id = db.Column(
        db.Integer,
        db.ForeignKey('members.id'),
        nullable=False,
    )
    share_count = db.Column(
        db.Integer,
        nullable=False,
    )
    share_per_amount = db.Column(
        db.Integer,
        nullable=False,
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
