from marshmallow import Schema, fields
from schemas.beneficiaries import BeneficiariesSchema
from schemas.shares import MemberSharesSchema


class LoanSchema(Schema):
    loan_amount = fields.Int()
    loan_payment_start_date = fields.Date()
    payment_term = fields.Int()
    status = fields.Str()
    uuid = fields.Str()
    created_at = fields.Date()


class RecommendedMemberSchema(Schema):
    first_name = fields.Str()
    middle_name = fields.Str()
    last_name = fields.Str()


class MemberSchema(Schema):
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
    loans = fields.List(
        fields.Nested(
            LoanSchema
        )
    )
    shares = fields.List(fields.Nested(MemberSharesSchema))
    beneficiaries = fields.List(fields.Nested(BeneficiariesSchema))
    recommended_by = fields.Nested(RecommendedMemberSchema)
