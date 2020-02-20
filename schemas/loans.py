from marshmallow import Schema, fields

from schemas.members import MemberSchema
from schemas.disbursments import DisbursmentsSchema


class RecieptSchema(Schema):

    uuid = fields.Str()
    reciept_type = fields.Str()
    loan_payment_term = fields.Int()
    or_number = fields.Str()
    amount = fields.Str()


class LoanSchema(Schema):
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
    disbursment = fields.Nested(
        DisbursmentsSchema
    )
    reciepts = fields.List(fields.Nested(
        RecieptSchema
    ))
    loan_amount = fields.Int()
    payment_term = fields.Int()
    service_charge = fields.Float()
    interest = fields.Float()
    capital_build_up = fields.Float()
    loan_payment_start_date = fields.Date()
    status = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
