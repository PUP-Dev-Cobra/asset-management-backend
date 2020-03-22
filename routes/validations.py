from flask import request, current_app, make_response
from flask_restful import Resource
import arrow

from internals.utils import token_required, user_check

from models.users import Users as UserModel
from models.members import Members as MemberModel
from models.loans import Loans as LoanModal


class EmailDuplicate(Resource):

    def get(self):
        try:
            email = request.args.get('email')

            userInfo = UserModel.query.filter_by(email=email).first()

            if (userInfo is not None):
                return {'error': 'email is already used'}

            return {'response': 'ok'}
        except NameError as e:
            return make_response({'error': 'Something is wrong' + e}, 500)


class LoanValidation(Resource):

    @token_required
    @user_check(user_type=['member'])
    def get(self, uuid):
        validationError = []
        try:
            memberInfo = MemberModel.query.filter_by(uuid=uuid).first()
            activeLoan = LoanModal\
                .query\
                .filter_by(member_id=memberInfo.id)\
                .filter_by(status='approved')\
                .all()

            # check if the user is one month old
            createdDate = arrow.get(memberInfo.created_at)
            dateNow = arrow.get()

            diff = dateNow - createdDate
            if (diff.days < 30):
                validationError\
                    .append('You need to be a member for at least 30 days.')

            # check member collateral
            if (memberInfo.available_collateral < 2000):
                validationError\
                    .append("You don't have enough collateral for another loan")

            # check if the active loan is paid 50%
            totalLoans = list(map(lambda x: x.net_loan_balance, activeLoan))
            paidAmount = list(map(lambda x: x.remaining_balance, activeLoan))
            sumOfTotalLoans = sum(totalLoans) if sum(totalLoans) > 0 else 1
            sumOfPaidAmount = sum(paidAmount)
            if (sumOfPaidAmount / sumOfTotalLoans) < 0.5:
                validationError\
                    .append("You haven't paid enough of your outstanding loans")

            return {'response': validationError}

        except NameError as e:
            print(e)
            return make_response({'error': 'Somethign is wrong'}, 500)
