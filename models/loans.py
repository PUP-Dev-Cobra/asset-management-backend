from internals.app import db


class Loans(db.Model):

  id = db.Column(
      db.Integer,
      primary_key=True,
      autoincrement=True,
      unique=True
  )
  uuid = db.Column(db.String(100), nullable=False, unique=True)
  member_id = db.Column(
      db.Integer,
      db.ForeignKey('members.id'),
      nullable=False
  )
  co_maker_1_id = db.Column(
      db.Integer,
      db.ForeignKey('members.id'),
      nullable=False
  )
  co_maker_2_id = db.Column(
      db.Integer,
      db.ForeignKey('members.id'),
      nullable=False
  )
  loan_amount = db.Column(
      db.Integer,
      nullable=False
  )
  payment_term = db.Column(
      db.Integer,
      nullable=False
  )
  service_charge = db.Column(
      db.Float,
      nullable=False
  )
  interest = db.Column(
      db.Float,
      nullable=False
  )
  capital_build_up = db.Column(
      db.Float,
      nullable=False
  )
  status = db.Column(
      db.String,
      nullable=False,
      default='draft'
  )
  created_at = db.Column(
      db.DATETIME,
      nullable=False
  )
  updated_at = db.Column(
      db.DATETIME,
      nullable=True
  )
  created_by = db.Column(
      db.Integer,
      nullable=False
  )
  updated_by = db.Column(
      db.Integer,
      nullable=True
  )
  member = db.relationship(
      'Members',
      foreign_keys=[member_id],
      uselist=False
  )
  co_maker_1 = db.relationship(
      'Members',
      foreign_keys=[co_maker_1_id],
      uselist=False
  )
  co_maker_2 = db.relationship(
      'Members',
      foreign_keys=[co_maker_2_id],
      uselist=False
  )
