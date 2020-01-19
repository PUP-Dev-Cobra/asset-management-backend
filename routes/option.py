from flask import request, jsonify, make_response, current_app
from flask_restful import Resource

from models.options import Options as OptionsModel, options_schema
from internals.utils import token_required, decode_token, user_check


class Options(Resource):

    @token_required
    def get(self):
        try:
            option_name = request.args.get('option_name')
            options = OptionsModel.query.filter_by(
                option_name=option_name).all()
            option_list = options_schema.dump(options)

            return {'response': option_list}
        except:
          return make_response({'error': 'Something is wrong'}, 500)
