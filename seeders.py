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
          name='Admin User',
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
    userType = [
        Options(option_name='user_type', option_value='teller'),
        Options(option_name='user_type', option_value='admin'),
        Options(option_name='user_type', option_value='approver'),
        Options(option_name='user_type', option_value='member'),
    ]
    gender = [
        Options(option_name='gender', option_value='male'),
        Options(option_name='gender', option_value='female')
    ]
    loanStatus = [
        Options(option_name='loan_status', option_value='draft'),
        Options(option_name='loan_status', option_value='pending'),
        Options(option_name='loan_status', option_value='approved'),
        Options(option_name='loan_status', option_value='rejected'),
        Options(option_name='loan_status', option_value='closed')
    ]
    civilStatus = [
        Options(option_name='civil_status', option_value='single'),
        Options(option_name='civil_status', option_value='married'),
        Options(option_name='civil_status', option_value='widow'),
    ]
    sourceOfIncome = [
        Options(option_name='source_of_income', option_value='1-5K'),
        Options(option_name='source_of_income', option_value='6-10K'),
        Options(option_name='source_of_income', option_value='11-20K'),
        Options(option_name='source_of_income', option_value='21-30K'),
        Options(option_name='source_of_income', option_value='31K++K'),
    ]
    paymentTerm = [
        Options(option_name='payment_term', option_value='1'),
        Options(option_name='payment_term', option_value='2'),
        Options(option_name='payment_term', option_value='3'),
        Options(option_name='payment_term', option_value='4'),
        Options(option_name='payment_term', option_value='5'),
        Options(option_name='payment_term', option_value='6'),
        Options(option_name='payment_term', option_value='7'),
        Options(option_name='payment_term', option_value='8'),
        Options(option_name='payment_term', option_value='9'),
        Options(option_name='payment_term', option_value='10'),
        Options(option_name='payment_term', option_value='11'),
        Options(option_name='payment_term', option_value='12'),
    ]
    serviceCharge = [
        Options(option_name='service_charge', option_value='2')
    ]
    interest = [
        Options(option_name='loan_interest', option_value='1.5')
    ]
    capitalBuildUp = [
        Options(option_name='captial_build_up', option_value='2')
    ]
    memberShareOption = [
        Options(option_name='share_per_amount', option_value='10')
    ]
    memberStatus = [
        Options(option_name='member_status', option_value='draft'),
        Options(option_name='member_status', option_value='pending'),
        Options(option_name='member_status', option_value='approved')
    ]
    loanCategory = [
        Options(option_name='loan_category', option_value='personal'),
        Options(option_name='loan_category', option_value='education'),
        Options(option_name='loan_category', option_value='housing'),
        Options(option_name='loan_category', option_value='medical'),
    ]
    dbs.bulk_save_objects(userStatus)
    dbs.bulk_save_objects(userType)
    dbs.bulk_save_objects(gender)
    dbs.bulk_save_objects(loanStatus)
    dbs.bulk_save_objects(civilStatus)
    dbs.bulk_save_objects(sourceOfIncome)
    dbs.bulk_save_objects(paymentTerm)
    dbs.bulk_save_objects(serviceCharge)
    dbs.bulk_save_objects(interest)
    dbs.bulk_save_objects(capitalBuildUp)
    dbs.bulk_save_objects(memberStatus)
    dbs.bulk_save_objects(memberShareOption)
    dbs.bulk_save_objects(loanCategory)
    dbs.commit()


seed_admin_user()
seed_options()
