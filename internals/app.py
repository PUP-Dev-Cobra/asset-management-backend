from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from internals.config import DevelopmentConfig
from flask_migrate import Migrate
from flask_cors import CORS
from flask_restful import Api

db = SQLAlchemy()
migrate = Migrate(compare_type=True)


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    api = Api(app)
    CORS(app)

    db.init_app(app)
    migrate.init_app(app, db)
    from models import users,\
        options,\
        members,\
        loans,\
        disbursments,\
        encashments,\
        reciepts,\
        invoices

    from routes import user,\
        option,\
        member,\
        loan,\
        disbrusment,\
        encashment,\
        reciept,\
        invoice,\
        validations,\
        shares

    api.add_resource(user.User, '/user', '/user/<string:uuid>')
    api.add_resource(user.List, '/user/list')
    api.add_resource(option.Options, '/options')
    api.add_resource(user.Authenticate, '/authenticate')
    api.add_resource(user.CreatePasswordResetHash, '/forgot-password')
    api.add_resource(user.ForgotPasswordReset, '/reset-password/<string:hash>')
    api.add_resource(member.Member, '/member', '/member/<string:uuid>')
    api.add_resource(member.MemberList, '/member/list')
    api.add_resource(loan.Loan, '/loan', '/loan/<string:uuid>')
    api.add_resource(loan.LoanList, '/loan/list')
    api.add_resource(loan.MemberLoanList, '/loan/members')
    api.add_resource(loan.MemberLoanShares, '/loan/member/share')
    api.add_resource(disbrusment.ListDisbursments, '/disbursment/list')
    api.add_resource(disbrusment.Disbursment, '/disbursment', '/disbursment/<string:uuid>')
    api.add_resource(encashment.Encashment, '/encashment', '/encashment/<string:uuid>')
    api.add_resource(encashment.EncashmentList, '/encashment/list')
    api.add_resource(reciept.Reciept, '/reciept', '/reciept/<string:uuid>')
    api.add_resource(reciept.RecieptList, '/reciept/list', '/reciept/list/<string:uuid>')
    api.add_resource(invoice.Invoice, '/invoice/<string:uuid>')
    api.add_resource(invoice.VoidInvoice, '/invoice/void/<string:uuid>')
    api.add_resource(shares.Shares, '/shares')

    # validations
    api.add_resource(validations.EmailDuplicate, '/validations/email-duplicate')
    api.add_resource(validations.LoanValidation, '/validations/loan-qualify/<string:uuid>')

    return app
