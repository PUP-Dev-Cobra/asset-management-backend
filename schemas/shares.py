from marshmallow import Schema, fields


class MemberSharesSchema(Schema):
  id = fields.Int()
  share_count = fields.Int()
  share_per_amount = fields.Int()
