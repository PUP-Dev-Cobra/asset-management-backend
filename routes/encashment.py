from flask import request, jsonify, make_response
from flask_restful import Resource
from datetime import datetime
from uuid import uuid4

from internals.app import db
from internals.utils import token_required, decode_token, user_check

from models.encashments import Encashments as EncashmentModel, encashment_schema
from models.disbursments import Disbursments as DisbursmentModel


class Encashment(Resource):

    @token_required
    @user_check(user_type=['teller'])
    def get(self, uuid):
        try:
            disbursmentData = DisbursmentModel\
                .query\
                .filter_by(uuid=uuid)\
                .first()
            encashmentData = EncashmentModel\
                .query\
                .filter_by(disbursment_id=disbursmentData.id)\
                .first()
            result = encashment_schema().dump(encashmentData)
            return {'response': result}
        except NameError as e:
            print(e)
            return make_response({'error': 'Something is wrong'}, 500)

    @token_required
    @user_check(user_type=['teller'])
    def post(self):
        params = request.get_json(force=True)
        userInfo = decode_token()

        try:
            disbursmentInfo = DisbursmentModel\
                .query\
                .filter_by(uuid=params.get('disbursment_id'))\
                .first()

            params = {
                'uuid': uuid4(),
                'disbursment_id': disbursmentInfo.id,
                'status': params.get('status'),
                'created_at': datetime.now(),
                'created_by_id': userInfo['id']
            }

            encashmentData = EncashmentModel(**params)
            db.session.add(encashmentData)
            db.session.commit()

            return {'response': encashmentData.uuid}
        except NameError:
            return make_response({'error': 'Something is wrong'}, 500)
