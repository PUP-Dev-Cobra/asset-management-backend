from flask import request, jsonify, make_response
from flask_restful import Resource
from datetime import datetime
from uuid import uuid4
import locale

from internals.app import db
from internals.utils import token_required, decode_token, user_check
from internals.mailgun import send_simple_message
from models.loans import Loans as LoanModel, loan_schema
from models.members import Members as MembersModel, member_schema
from models.shares import MemberShares as MemberShareModal

from pathlib import Path


class Loan(Resource):

    @token_required
    @user_check(user_type=['teller', 'approver', 'member'])
    def get(self, uuid):
        try:
            loans = LoanModel.query.filter_by(uuid=uuid).first()
            results = loan_schema().dump(loans)
            return {'response': results}
        except NameError as e:
            print(e)
            return {'error': 'Something went wrong'}

    @token_required
    @user_check(user_type=['approver', 'member'])
    def post(self):
        params = request.get_json(force=True)
        userInfo = decode_token()

        if userInfo['user_type'] == 'member':
            params['status'] = 'pending'

        if "member_id" in params:
            clientInfo = MembersModel\
                .query\
                .filter_by(uuid=params['member_id'])\
                .first()
            params['member_id'] = clientInfo.id

        if "co_maker_1_id" in params:
            memberInfo = MembersModel\
                .query\
                .filter_by(uuid=params['co_maker_1_id'])\
                .first()
            params['co_maker_1_id'] = memberInfo.id

        if "co_maker_2_id" in params:
            memberInfo = MembersModel\
                .query\
                .filter_by(uuid=params.get('co_maker_2_id'))\
                .first()
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

            send_simple_message(
                subject='Your %s Loan Application For  Created' % (params['loan_category']),
                text=Path('./templates/loanapplication.template.html')
                .read_text()
                .replace("{{name}}", clientInfo.first_name)
                .replace("{{category}}", params['loan_category'])
                .replace("{{amount}}", locale.format('%.2f', params['loan_amount'], grouping=True))
            )

            db.session.commit()

            return {'response': loanParams.uuid}
        except NameError:
            return make_response({'error': 'Something is wrong'}, 500)

    @token_required
    @user_check(user_type=['member', 'approver'])
    def put(self, uuid):
        params = request.get_json(force=True)
        userInfo = decode_token()
        userType = userInfo.get('user_type')

        if "member_id" in params:
            clientInfo = MembersModel.query.filter_by(uuid=params['member_id']).first()
            params['member_id'] = clientInfo.id

        if "co_maker_1_id" in params and userType == 'member':
            memberInfo = MembersModel.query.filter_by(uuid=params.get('co_maker_1_id')).first()
            params['co_maker_1_id'] = memberInfo.id

        if "co_maker_2_id" in params and userType == 'member':
            memberInfo = MembersModel.query.filter_by(uuid=params.get('co_maker_2_id')).first()
            params['co_maker_2_id'] = memberInfo.id

        updateParmas = {
            **params,
            'updated_at': datetime.now(),
            'updated_by_id': userInfo['id']
        }

        try:
            LoanModel.query.filter_by(uuid=uuid).update(updateParmas)
            loanInfo = LoanModel.query.filter_by(uuid=uuid).first()

            if userInfo['user_type'] == 'approver' \
                    and params['status'] == 'approved':
                # create a negative share as collateral
                share_count = loanInfo.loan_amount / loanInfo.share_amount
                shareParams = {
                    'member_id': clientInfo.id,
                    'share_count': share_count * -1,
                    'share_per_amount': loanInfo.share_amount,
                    'created_at': datetime.now(),
                    'created_by_id': userInfo['id']
                }
                db.session.add(MemberShareModal(**shareParams))

            if userInfo['user_type'] == 'member':
                send_simple_message(
                    subject='Your %s Loan Application For is Updated' % (params['loan_category']),
                    text=Path('./templates/loanapplicationupdate.template.html')
                    .read_text()
                    .replace("{{name}}", clientInfo.first_name)
                    .replace("{{category}}", params['loan_category'])
                    .replace("{{amount}}", locale.format('%.2f', params['loan_amount'], grouping=True))
                )

            if userInfo['user_type'] == 'approver':
                send_simple_message(
                    subject='Your %s Loan Application For is %s' % (loanInfo.loan_category, params['status']),
                    text=Path('./templates/loanapplicationstatus.template.html')
                    .read_text()
                    .replace("{{name}}", clientInfo.first_name)
                    .replace("{{category}}", loanInfo.loan_category)
                    .replace("{{status}}", params['status'])
                    .replace("{{amount}}", locale.format('%.2f', loanInfo.loan_amount, grouping=True))
                )

            db.session.commit()

            return {'response': True}
        except NameError as e:
            print(e)
            return make_response({'error': 'Something is wrong'}, 500)


class LoanList(Resource):

    @token_required
    @user_check(user_type=['teller', 'approver'])
    def get(self):
        try:
            loans = LoanModel\
                .query\
                .order_by(
                    LoanModel.status.desc(),
                    LoanModel.updated_at.desc(),
                    LoanModel.created_at.desc()
                )\
                .all()
            result = loan_schema(
                many=True,
                only=[
                    'uuid',
                    'member',
                    'loan_amount',
                    'status',
                    'loan_category',
                    'remaining_balance',
                    'created_at',
                    'updated_at'
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
                .order_by(MembersModel.last_name)\
                .all()
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
