from sqlalchemy.ext.hybrid import hybrid_property

from internals.app import db
from schemas.loans import LoanSchema
from flask_sqlalchemy import sqlalchemy

backref = sqlalchemy.orm.backref
desc = sqlalchemy.desc


class Loans(db.Model):

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
    co_maker_1_id = db.Column(
        db.Integer,
        db.ForeignKey('members.id'),
        nullable=True
    )
    co_maker_2_id = db.Column(
        db.Integer,
        db.ForeignKey('members.id'),
        nullable=True
    )
    loan_amount = db.Column(
        db.Integer,
        nullable=False
    )
    payment_term = db.Column(
        db.Integer,
        nullable=False
    )
    service_charge = db.Column(
        db.Float,
        nullable=False
    )
    interest = db.Column(
        db.Float,
        nullable=False
    )
    capital_build_up = db.Column(
        db.Float,
        nullable=False
    )
    status = db.Column(
        db.String,
        nullable=False,
        default='draft'
    )
    share_amount = db.Column(
        db.Integer,
        nullable=False
    )
    loan_category = db.Column(
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
        nullable=False
    )
    updated_by_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=True
    )
    member = db.relationship(
        'Members',
        foreign_keys=[member_id],
        uselist=False
    )
    co_maker_1 = db.relationship(
        'Members',
        foreign_keys=[co_maker_1_id],
        uselist=False
    )
    co_maker_2 = db.relationship(
        'Members',
        foreign_keys=[co_maker_2_id],
        uselist=False
    )
    loanInvoice = db.relationship(
        'Invoices',
        lazy=True,
        backref=backref('loanInfo', order_by=desc('Invoices.created_at'))
    )
    disbursment = db.relationship(
        'Disbursments',
        lazy=True,
        uselist=False,
        backref='loanInfo'
    )
    reciepts = db.relationship(
        'Reciepts',
        backref='loanInfo',
        lazy=True
    )

    @hybrid_property
    def net_loan_balance(self):
        loan_amount = self.loan_amount
        interest = (loan_amount * (self.interest / 100)) * self.payment_term
        service_charge = loan_amount * (self.service_charge / 100)
        capital_build = loan_amount * (self.capital_build_up / 100)
        return loan_amount - interest - service_charge - capital_build

    @hybrid_property
    def net_loan_per_month(self):
        return self.net_loan_balance / self.payment_term

    @hybrid_property
    def remaining_balance(self):
        paidAmount = list(map(lambda x: x.amount, self.reciepts))
        return self.net_loan_balance - sum(paidAmount)

    @hybrid_property
    def capital_build_up_amount(self):
        loan_amount = self.loan_amount
        capital_build = loan_amount * (self.capital_build_up / 100)
        return capital_build


def loan_schema(many=False, **kwargs):
    return LoanSchema(many=many, **kwargs)
