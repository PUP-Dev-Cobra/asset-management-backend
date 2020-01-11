from internals.app import db


class Options(db.model):
  id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
  option_name = db.Column(db.String)
  option_value = db.Column(db.String)
