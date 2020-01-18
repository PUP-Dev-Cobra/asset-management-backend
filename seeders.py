#!/usr/bin/env python3

from internals.app import create_app
from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4
from datetime import datetime

from models.users import Users
from models.options import Options

app = create_app()
db = SQLAlchemy()


def seed_admin_user():
  with app.app_context():
    ifAdminExist = Users.query.filter_by(email='admin@mail.com').first()
    if (ifAdminExist is None):
      admin = Users(
          uuid=uuid4(),
          email='admin@mail.com',
          password=Users.hashPassword('Test2019'),
          user_type='admin',
          status='active',
          created_at=datetime.now(),
          created_by_id=None
      )
      db.session.add(admin)
      db.session.commit()
    else:
      print('Admin alredy exist')


def seed_options():
  """
    Do not execute this if the option table is already added
  """
  with app.app_context():
    dbs = db.session
    userStatus = [
        Options(option_name='user_status', option_value='active'),
        Options(option_name='user_status', option_value='disable'),
        Options(option_name='user_status', option_value='pending')
    ]
    gender = [
        Options(option_name='gender', option_value='male'),
        Options(option_name='gender', option_value='female')
    ]
    loanStatus = [
        Options(option_name='loan_status', option_value='draft'),
        Options(option_name='loan_status', option_value='pending_approval'),
        Options(option_name='loan_status', option_value='approved'),
        Options(option_name='loan_status', option_value='rejected'),
        Options(option_name='loan_status', option_value='closed'),
        Options(option_name='loan_status', option_value='default')
    ]
    dbs.bulk_save_objects(userStatus)
    dbs.bulk_save_objects(gender)
    dbs.bulk_save_objects(loanStatus)
    dbs.commit()


seed_admin_user()
seed_options()
