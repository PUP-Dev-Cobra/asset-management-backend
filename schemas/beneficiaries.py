from marshmallow import Schema, fields


class BeneficiariesSchema(Schema):
  id = fields.Int()
  first_name = fields.Str()
  last_name = fields.Str()
  middle_name = fields.Str()
  relationship = fields.Str()
  dob = fields.Date()
