from flask import request, jsonify, make_response
from flask_restful import Resource
from datetime import datetime
from uuid import uuid4
import locale

from internals.app import db
from internals.mailgun import send_simple_message
from internals.utils import token_required, decode_token, user_check

from models.loans import Loans as LoanModel
from models.disbursments import Disbursments as DisbursmentsModel, disbursment_schema

from pathlib import Path


class Disbursment(Resource):

    @token_required
    @user_check(user_type=['teller'])
    def get(self, uuid):
        try:
            loanData = LoanModel.query.filter_by(uuid=uuid).first()
            disbursment = DisbursmentsModel\
                .query\
                .filter(DisbursmentsModel.loan_id == loanData.id)\
                .filter(DisbursmentsModel.status == 'issued')\
                .first()
            results = disbursment_schema().dump(disbursment)
            return {'response': results}
        except NameError:
            return make_response({'error': 'Something is wrong'}, 500)

    @token_required
    @user_check(user_type=['teller'])
    def post(self):
        params = request.get_json(force=True)
        userInfo = decode_token()

        try:
            loanData = LoanModel\
                .query\
                .filter_by(uuid=params.get('uuid'))\
                .first()
            params = {
                **params,
                'uuid': uuid4(),
                'loan_id': loanData.id,
                'created_at': datetime.now(),
                'created_by_id': userInfo['id']
            }
            disbursmentData = DisbursmentsModel(**params)
            db.session.add(disbursmentData)

            # Send disbursment status notification
            send_simple_message(
                subject="%s Cheque is Ready" % (loanData.member.first_name),
                text=Path('./templates/loanapplication.template.html')
                .read_text()
                .replace("{{name}}", loanData.member.first_name)
                .replace("{{statys}}", "Ready")
                .replace("{{amount}}", locale.format('%.2f', loanData.net_loan_balance, grouping=True))
            )

            db.session.commit()

            return {'response': disbursmentData.uuid}
        except NameError:
            return make_response({'error': 'Something is wrong'}, 500)

    @token_required
    @user_check(user_type=['teller'])
    def put(self, uuid):
        params = request.get_json(force=True)
        userInfo = decode_token()

        # We only need the status
        params = {
            'status': params.get('status'),
            'updated_at': datetime.now(),
            'updated_by_id': userInfo['id']
        }

        try:
            DisbursmentsModel\
                .query\
                .filter_by(uuid=uuid)\
                .update(params)
            db.session.commit()
            return {'response': True}
        except NameError:
            return make_response({'error': 'Something is wrong'}, 500)


class ListDisbursments(Resource):

    @token_required
    @user_check(user_type=['teller'])
    def get(self):
        try:
            disbursmentsData = DisbursmentsModel.query.all()
            result = disbursment_schema(many=True).dump(disbursmentsData)

            return {'response': result}
        except NameError:
            return make_response({'response': 'Something is wrong'}, 500)
