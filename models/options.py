from internals.app import db
from marshmallow import Schema, fields


class Options(db.Model):
  id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
  option_name = db.Column(db.String)
  option_value = db.Column(db.String)


class OptionsSchema(Schema):
  option_name = fields.Str()
  option_value = fields.Str()


option_schema = OptionsSchema()
options_schema = OptionsSchema(many=True)
