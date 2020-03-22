from flask import request, jsonify, make_response
from flask_restful import Resource
from datetime import datetime
from uuid import uuid4

from internals.app import db
from internals.utils import token_required, decode_token, user_check

from models.invoices import Invoices as InvoiceModel
from models.members import Members as MemberModel


class Shares(Resource):

    @token_required
    @user_check(user_type=['member'])
    def post(self):
        params = request.get_json(force=True)
        userInfo = decode_token()

        try:
            memberInfo = MemberModel\
                .query\
                .filter_by(uuid=params['member_id'])\
                .first()

            newParams = {
                **params,
                'uuid': uuid4(),
                'member_id': memberInfo.id,
                'status': 'pending',
                'created_by_id': userInfo['id']
            }

            InvoiceModel()\
                .createInvoice(
                invoiceInfo=newParams,
                name=memberInfo.first_name
            )

            return {'response': True}
        except NameError as e:
            print(e)
            return make_response({'error': 'Something is wrong'}, 500)
