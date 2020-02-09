from marshmallow import Schema, fields
from schemas.disbursments import DisbursmentsSchema


class EncashmentSchema(Schema):
  uuid = fields.Str()
  disbursmentInfo = fields.Nested(DisbursmentsSchema)
  created_at = fields.DateTime()
