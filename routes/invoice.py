from flask import request, jsonify, make_response
from flask_restful import Resource
from datetime import datetime
from uuid import uuid4
from pathlib import Path
import locale

from internals.app import db
from internals.mailgun import send_simple_message
from internals.utils import token_required, decode_token, user_check

from models.invoices import Invoices as InvoiceModel
from models.reciepts import Reciepts as RecieptModel
from models.members import Members as MemberModal
from models.shares import MemberShares as MemberSharesModel
from models.loans import Loans as LoanModel


class Invoice(Resource):

    @token_required
    @user_check(user_type=['teller'])
    def post(self, uuid):
        params = request.get_json(force=True)
        userInfo = decode_token()

        if uuid is None:
            return make_response({'error': 'No uuid'}, 500)

        try:
            invoiceParams = {
                'status': 'paid',
                'updated_at': datetime.now(),
                'updated_by_id': userInfo['id']
            }
            InvoiceModel\
                .query\
                .filter_by(uuid=uuid)\
                .update(invoiceParams)

            loan_id = params['loan_id']
            invoice_type = params['invoice_type']

            # add share once the member is paid
            if invoice_type == 'shares':
                collateral = float(params['amount'])
                shareParams = {
                    'member_id': params['member_id'],
                    'share_count': collateral / 10,
                    'share_per_amount': 10,
                    'created_at': datetime.now(),
                    'created_by_id': userInfo['id']
                }
                db.session.add(MemberSharesModel(**shareParams))

            # check if we need to close the loan
            if invoice_type == 'loan':
                loanInfo = LoanModel.query.filter_by(id=loan_id).first()
                remainingBalance = loanInfo.remaining_balance - float(params['amount'])
                if (remainingBalance <= 0):
                    loanParams = {
                        'status': 'paid',
                        'updated_at': datetime.now(),
                        'updated_by_id': userInfo['id']
                    }
                    LoanModel.query.filter_by(id=loan_id).update(loanParams)

                    # Release the collateral/shares
                    newShares = loanInfo.loan_amount + loanInfo.capital_build_up_amount
                    sharesMember = {
                        'member_id': params['member_id'],
                        'share_count': newShares / loanInfo.share_amount,
                        'share_per_amount': loanInfo.share_amount,
                        'created_at': datetime.now(),
                        'created_by_id': userInfo['id']
                    }
                    db.session.add(MemberSharesModel(**sharesMember))

                    # Release the collateral of co-makers WIP

            # Create reciept
            recieptParams = {
                'uuid': uuid4(),
                'reciept_type': invoice_type,
                'loan_id': loan_id,
                'or_number': params['or_number'],
                'amount': params['amount'],
                'invoice_id': params['invoice_id'],
                'created_at': datetime.now(),
                'created_by_id': userInfo['id']
            }
            recieptInfo = RecieptModel(**recieptParams)
            db.session.add(recieptInfo)

            # Send email to recepient
            invoiceInfo = InvoiceModel.query.filter_by(uuid=uuid).first()
            send_simple_message(
                subject='Thank your for your payment',
                text=Path('./templates/payment.template.html')
                .read_text()
                .replace("{{name}}", invoiceInfo.memberInfo.first_name)
                .replace("{{invoiceType}}", invoice_type)
                .replace("{{type}}", invoice_type)
                .replace("{{amount}}", locale.format('%.2f', params['amount']))
            )

            db.session.commit()
            return {'response': 'ok'}

        except NameError as e:
            print(e)
            return make_response({'error': 'Something is wrong'}, 500)


class VoidInvoice(Resource):

    @token_required
    @user_check(user_type=['member'])
    def post(self, uuid):
        params = request.get_json(force=True)
        userInfo = decode_token()

        try:
            memberInfo = MemberModal\
                .query\
                .filter_by(uuid=params['member_id'])\
                .first()

            newParams = {
                'status': 'void',
                'updated_by_id': userInfo['id'],
                'updated_at': datetime.now()
            }

            emailParams = {
                'invoice_type': params['invoice_type'],
                'amount': float(params['amount'])
            }

            InvoiceModel().voidInvoice(
                uuid=uuid,
                invoiceInfo=newParams,
                params=emailParams,
                name=memberInfo.first_name
            )

            return {'response': True}
        except NameError as e:
            print(e)
            return make_response({'error': 'Something is wrong'}, 500)
