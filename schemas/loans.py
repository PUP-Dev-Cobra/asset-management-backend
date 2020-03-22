from marshmallow import Schema, fields
from sqlalchemy.ext.hybrid import hybrid_property

from schemas.members import MemberSchema
from schemas.disbursments import DisbursmentsSchema


class RecieptSchema(Schema):

    uuid = fields.Str()
    reciept_type = fields.Str()
    loan_payment_term = fields.Int()
    or_number = fields.Str()
    amount = fields.Str()
    created_at = fields.DateTime()


memberFields = [
    'first_name',
    'last_name',
    'middle_name',
    'dob',
    'uuid',
    'available_collateral'
]


class LoanSchema(Schema):
    uuid = fields.Str()
    member = fields.Nested(
        MemberSchema,
        only=memberFields
    )
    co_maker_1 = fields.Nested(
        MemberSchema,
        only=memberFields
    )
    co_maker_2 = fields.Nested(
        MemberSchema,
        only=memberFields
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
    net_loan_balance = fields.Float()
    net_loan_per_month = fields.Float()
    remaining_balance = fields.Float()
    loan_category = fields.Str()
    status = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
