#!/usr/bin/env python3

from internals.app import create_app
from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4
from datetime import datetime
import arrow

from models.loans import Loans as LoanModel
from models.invoices import Invoices as InvoiceModel

app = create_app()
db = SQLAlchemy()


def generate_invoice():
    with app.app_context():
        dbs = db.session
        datenow = arrow.utcnow()

        # Look for active loans
        loans = LoanModel.query.filter_by(status='approved').all()
        for loan in loans:
            paymentTerm = loan.payment_term
            invoices = loan.loanInvoice

            # See if there is already a generated invoice for that month
            if (len(invoices) > 0):
                invoiceDate = arrow.get(invoices[0].created_at)
                if invoiceDate.month == datenow.month:
                    print("invoices are already made for this month")
                    break

            # see if the this needs more invoice
            if (len(invoices) >= paymentTerm):
                print("No invoices are needed now")
                break

            # generate invoice
            loanAmount = loan.loan_amount
            serviceCharge = loan.service_charge
            capitalBuildUp = loan.capital_build_up
            interest = loan.interest

            netAmount = loanAmount - (loanAmount * serviceCharge / 100) \
                - (loanAmount * capitalBuildUp / 100) \
                - (loanAmount * (interest / 100 * paymentTerm)) \
                / paymentTerm

            params = {
                'uuid': uuid4(),
                'member_id': loan.member_id,
                'loan_id': loan.id,
                'invoice_type': 'loan',
                'amount': netAmount,
                'status': 'pending',
                'created_at': datetime.now(),
                'created_by_id': None
            }

            dbs.add(InvoiceModel(**params))

        dbs.commit()


generate_invoice()
