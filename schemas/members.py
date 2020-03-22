from marshmallow import Schema, fields
from schemas.beneficiaries import BeneficiariesSchema
from schemas.shares import MemberSharesSchema
<<<<<<< HEAD
=======
from schemas.users import UserSchema
from schemas.invoices import InvoiceSchema
>>>>>>> 6cec8ea... Invoice and approving


class LoanSchema(Schema):
    loan_amount = fields.Int()
    loan_payment_start_date = fields.Date()
    payment_term = fields.Int()
    status = fields.Str()
    uuid = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()


class RecommendedMemberSchema(Schema):
    first_name = fields.Str()
    middle_name = fields.Str()
    last_name = fields.Str()


class InvoiceReciept(Schema):
    uuid = fields.Str()
    reciept_type = fields.Str()
    loan_payment_term = fields.Int()
    or_number = fields.Str()
    amount = fields.Float()
    created_at = fields.DateTime()


class MemberSchema(Schema):
    id = fields.Int()
    address = fields.Str()
    age = fields.Int()
    civil_status = fields.Str()
    contact_no = fields.Str()
    dob = fields.Date()
    first_name = fields.Str()
    gender = fields.Str()
    last_name = fields.Str()
    middle_name = fields.Str()
    monthly_income = fields.Str()
    nickname = fields.Str()
    religion = fields.Str()
    source_of_income = fields.Str()
    spouse_name = fields.Str()
    status = fields.Str()
    tin_oca = fields.Str()
    uuid = fields.Str()
    outstanding_invoice = fields.Float()
    available_collateral = fields.Float()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    loans = fields.List(
        fields.Nested(
            LoanSchema
        )
    )
<<<<<<< HEAD
=======
    invoices = fields.List(
        fields.Nested(
            InvoiceSchema
        )
    )
    reciepts = fields.List(fields.Nested(InvoiceReciept))
    userInfo = fields.Nested(UserSchema, only=['email'])
>>>>>>> 6cec8ea... Invoice and approving
    shares = fields.List(fields.Nested(MemberSharesSchema))
    beneficiaries = fields.List(fields.Nested(BeneficiariesSchema))
    recommended_by = fields.Nested(RecommendedMemberSchema)
