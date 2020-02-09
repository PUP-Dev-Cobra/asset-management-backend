from flask import request, jsonify, make_response
from flask_restful import Resource
from datetime import datetime
from uuid import uuid4

from internals.app import db
from internals.utils import token_required, decode_token, user_check

from models.members import Members as MembersModel
from models.reciepts import Reciepts as RecieptsModel, reciept_schema
from models.loans import Loans as LoansModel


class Reciept(Resource):

    @token_required
    @user_check(user_type=['teller'])
    def post(self):
        # Add cheker later. For now standard post
        params = request.get_json(force=True)
        userInfo = decode_token()

        try:
            loanInfo = LoansModel\
                .query\
                .filter_by(uuid=params['loan_id'])\
                .first()
            params['loan_id'] = loanInfo.id
            params = {
                **params,
                'uuid': uuid4(),
                'created_at': datetime.now(),
                'created_by_id': userInfo['id']
            }
            recieptInfo = RecieptsModel(**params)
            db.session.add(recieptInfo)
            db.session.commit()

            return {'response': recieptInfo.uuid}
        except NameError:
            return make_response({'error': 'Something is wrong'}, 500)


class RecieptList(Resource):

    @token_required
    @user_check(user_type=['teller'])
    def get(self, uuid):
        try:
            recieptInfo = RecieptsModel.query
            if (uuid):
                memberInfo = MembersModel.query.filter_by(uuid=uuid).first()
                recieptInfo = recieptInfo\
                    .join(LoansModel)\
                    .filter_by(member_id=memberInfo.id)
            recieptInfo = recieptInfo.all()
            result = reciept_schema(many=True).dump(recieptInfo)
            return {'response': result}
        except NameError as e:
            print(e)
            return make_response({'error': 'Somethign is wrong'}, 500)
