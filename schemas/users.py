from marshmallow import Schema, fields


class UserSchema(Schema):
    uuid = fields.Str()
    name = fields.Str()
    email = fields.Email()
    status = fields.Str()
    user_type = fields.Str()
<<<<<<< HEAD
    member_id = fields.Int()
=======
>>>>>>> fe09d7bedf8dece4168af3544b433310dd84c921
    updated_at = fields.DateTime()
    created_at = fields.DateTime()
