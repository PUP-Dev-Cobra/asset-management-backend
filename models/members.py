from marshmallow import Schema, fields
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import desc, case

from internals.app import db
from models.users import Users
from models.loans import Loans
from models.beneficiaries import Beneficiaries
from models.shares import MemberShares
from models.invoices import Invoices
from models.reciepts import Reciepts
from schemas.members import MemberSchema

invoice_order = case([(Invoices.status == 'pending', 0), (Invoices.status == 'paid', 1), (Invoices.status == 'void', 2)], None)
loan_order = case([(Loans.status == 'pending', 0), (Loans.status == 'void', 1), (Loans.status == 'paid', 2)], None)
reciept_order = case([(Reciepts.reciept_type == 'loan', 0), (Reciepts.reciept_type == 'shares', 1), (Reciepts.reciept_type == 'membership', 2)], None)


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
        foreign_keys=[Loans.member_id],
        order_by=[loan_order, desc(Loans.created_at)]
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
    userInfo = db.relationship(
        Users,
        lazy=True,
        backref='memberInfo',
        foreign_keys=[Users.member_id]
    )
    invoices = db.relationship(
        Invoices,
        lazy=True,
        backref='memberInfo',
        order_by=[invoice_order, desc(Invoices.created_at)],
        foreign_keys=[Invoices.member_id]
    )

    @hybrid_property
    def reciepts(self):
        return db.session.query(Reciepts)\
            .join(Invoices)\
            .filter(Invoices.member_id == self.id)\
            .filter(Invoices.id == Reciepts.invoice_id)\
            .order_by(reciept_order)\
            .order_by(desc(Reciepts.created_at))\
            .all()

    @hybrid_property
    def outstanding_invoice(self):
        unpaidInvoices = list(filter(lambda x: x.status == 'pending', self.invoices))
        values = list(map(lambda x: x.amount, unpaidInvoices))
        return sum(values)

    @hybrid_property
    def available_collateral(self):
        values = list(map(lambda x: x.share_count * x.share_per_amount, self.shares))
        return sum(values)


def member_schema(many=False, **kwargs):
    return MemberSchema(many=many, **kwargs)
