from marshmallow import Schema, fields
from schemas.members import MemberSchema


class LoanDisbursmentSchema(Schema):
    uuid = fields.Str()
    member = fields.Nested(
        MemberSchema,
        only=['first_name', 'last_name', 'middle_name', 'dob', 'uuid']
    )
    co_maker_1 = fields.Nested(
        MemberSchema, 
        only=['first_name', 'last_name', 'middle_name', 'dob', 'uuid']
    )
    co_maker_2 = fields.Nested(
        MemberSchema, 
        only=['first_name', 'last_name', 'middle_name', 'dob', 'uuid']
    )
    net_loan_balance = fields.Float()


class DisbursmentsSchema(Schema):
    uuid = fields.Str()
    loanInfo = fields.Nested(LoanDisbursmentSchema)
    check_voucher = fields.Str()
    check_number = fields.Str()
    status = fields.Str()
    issue_date = fields.Date()
    signatory = fields.Str()
    created_at = fields.Date()
