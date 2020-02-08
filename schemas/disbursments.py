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
    loan_amount = fields.Method('disbursed_amount')

    def disbursed_amount(self, obj):
        interestAmount = obj.loan_amount * ((obj.interest / 100) * obj.payment_term)
        service_charge = obj.loan_amount * (obj.service_charge / 100)
        capital_buildup = obj.loan_amount * (obj.capital_build_up / 100)
        return obj.loan_amount - interestAmount - service_charge - capital_buildup


class DisbursmentsSchema(Schema):
    uuid = fields.Str()
    loanInfo = fields.Nested(LoanDisbursmentSchema)
    check_voucher = fields.Str()
    check_number = fields.Str()
    status = fields.Str()
    created_at = fields.Date()
