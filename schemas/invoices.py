from marshmallow import Schema, fields


class InvoiceSchema(Schema):

    id = fields.Int()
    uuid = fields.Str()
    member_id = fields.Int()
    invoice_type = fields.Str()
    loan_id = fields.Int()
    amount = fields.Float()
    status = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
