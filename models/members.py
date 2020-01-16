from internals.app import db
from models.loans import Loans


class Members(db.Model):

  id = db.Column(
      db.Integer,
      primary_key=True,
      autoincrement=True,
      unique=True
  )
  uuid = db.Column(db.String(100), nullable=False, unique=True)
  first_name = db.Column(db.String, nullable=False)
  last_name = db.Column(db.String, nullable=False)
  middle_name = db.Column(db.String, nullable=True)
  nickname = db.Column(db.String, nullable=False)
  first_name = db.Column(db.String, nullable=False)
  dob = db.Column(db.Date, nullable=False)
  age = db.Column(db.Integer, nullable=False)
  gender = db.Column(db.String, nullable=False)
  first_name = db.Column(db.String, nullable=False)
  civil_status = db.Column(db.String, nullable=False)
  address = db.Column(db.String, nullable=False)
  contact_no = db.Column(db.String, nullable=False)
  tin_oca = db.Column(db.String, nullable=True)
  status = db.Column(db.String, nullable=False)
  loans = db.relationship('Loans', lazy=True, foreign_keys=[Loans.member_id])
