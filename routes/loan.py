from flask import request, jsonify, make_response
from flask_restful import Resource
from datetime import datetime
from uuid import uuid4

from internals.app import db
from internals.utils import token_required, decode_token, user_check
from models.loans import Loans as LoanModel, loan_schema
from models.members import Members as MembersModel, member_schema


class Loan(Resource):

    @token_required
    @user_check(user_type=['teller', 'approver', 'member'])
    def get(self, uuid):
        try:
            loans = LoanModel.query.filter_by(uuid=uuid).first()
            results = loan_schema().dump(loans)
            return {'response': results}
        except:
            return {'error': 'Something went wrong'}

    @token_required
    @user_check(user_type=['teller'])
    def post(self):
        # Add checkers later. For now just standard post
        params = request.get_json(force=True)
        userInfo = decode_token()

        if "member_id" in params:
            memberInfo = MembersModel.query.filter_by(uuid=params.get('member_id')).first()
            params['member_id'] = memberInfo.id

        if "co_maker_1_id" in params:
            memberInfo = MembersModel.query.filter_by(uuid=params.get('co_maker_1_id')).first()
            params['co_maker_1_id'] = memberInfo.id

        if "co_maker_2_id" in params:
            memberInfo = MembersModel.query.filter_by(uuid=params.get('co_maker_2_id')).first()
            params['co_maker_2_id'] = memberInfo.id

        params = {
            **params,
            'uuid': uuid4(),
            'created_at': datetime.now(),
            'created_by_id': userInfo['id']
        }

        try:
            loanParams = LoanModel(**params)
            db.session.add(loanParams)
            db.session.commit()

            return {'response': loanParams.uuid}
        except NameError:
            return make_response({'error': 'Something is wrong'}, 500)

    @token_required
    @user_check(user_type=['teller', 'approver'])
    def put(self, uuid):
        params = request.get_json(force=True)
        userInfo = decode_token()
        userType = userInfo.get('user_type')

        print(userType)
        if "member_id" in params and userType == 'teller':
            memberInfo = MembersModel.query.filter_by(uuid=params.get('member_id')).first()
            params['member_id'] = memberInfo.id

        if "co_maker_1_id" in params and userType == 'teller':
            memberInfo = MembersModel.query.filter_by(uuid=params.get('co_maker_1_id')).first()
            params['co_maker_1_id'] = memberInfo.id

        if "co_maker_2_id" in params and userType == 'teller':
            memberInfo = MembersModel.query.filter_by(uuid=params.get('co_maker_2_id')).first()
            params['co_maker_2_id'] = memberInfo.id

        updateParmas = {
            **params,
            'updated_at': datetime.now(),
            'updated_by_id': userInfo['id']
        }

        try:
            LoanModel.query.filter_by(uuid=uuid).update(updateParmas)
            db.session.commit()

            return {'response': True}
        except NameError:
            return make_response({'error': 'Something is wrong'}, 500)


class LoanList(Resource):

    @token_required
    @user_check(user_type=['teller', 'approver'])
    def get(self):
        try:
            loans = LoanModel.query.all()
            result = loan_schema(
                many=True,
                only=[
                    'uuid',
                    'member',
                    'loan_amount',
                    'status',
                    'loan_payment_start_date'
                ])\
                .dump(loans)

            return {'response': result}
        except Exception as e:
            print(e)
            return make_response({'error': 'Something is wrong'}, 500)


class MemberLoanList(Resource):

    @token_required
    @user_check(user_type=['teller', 'approver', 'member'])
    def get(self):
        try:
            members = MembersModel\
                .query\
                .filter_by(status='approved')\
                .order_by(MembersModel.last_name).all()
            result = member_schema(many=True, only=[
                "uuid",
                "first_name",
                "last_name",
                "middle_name"
            ]).dump(members)

            return {'response': result}
        except Exception as e:
            return make_response({'error': e}, 500)


class MemberLoanShares(Resource):

    # Fetch the member shares
    @token_required
    @user_check(user_type=['teller', 'approver', 'member'])
    def get(self):
        try:
            uuid = request.args.get('uuid')
            member = MembersModel.query.filter_by(uuid=uuid).first()
            result = member_schema(only=['shares']).dump(member)

            return {'response': result}
        except Exception as e:
            return make_response({'error': e}, 500)
