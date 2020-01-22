from marshmallow import Schema, fields


class DisbursmentsSchema(Schema):
    uuid = fields.Str()
    check_voucher = fields.Str()
    check_number = fields.Str()
    status = fields.Str()
    created_at = fields.Date()
