from marshmallow import Schema, fields

from schemas.loans import LoanSchema


class RecieptSchema(Schema):

    uuid = fields.Str()
    transaction_type = fields.Str()
    loanInfo = fields.Nested(
        LoanSchema,
        only=['uuid', 'member', 'co_maker_1', 'co_maker_2']
    )
    loan_payment_term = fields.Int()
    or_number = fields.Str()
    amount = fields.Float()
    created_at = fields.DateTime()
