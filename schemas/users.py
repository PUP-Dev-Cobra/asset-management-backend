from marshmallow import Schema, fields


class UserSchema(Schema):
    uuid = fields.Str()
    name = fields.Str()
    email = fields.Email()
    status = fields.Str()
    user_type = fields.Str()
    updated_at = fields.DateTime()
    created_at = fields.DateTime()
