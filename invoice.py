#!/usr/bin/env python3

from internals.app import create_app
from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4
from datetime import datetime
import arrow

from models.loans import Loans as LoanModel
from models.invoices import Invoices as InvoiceModel

app = create_app()


def generate_invoice():
    with app.app_context():
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
                    continue

            # see if the this needs more invoice
            if (len(invoices) >= paymentTerm):
                print("No invoices are needed now")
                continue

            params = {
                'uuid': uuid4(),
                'member_id': loan.member_id,
                'loan_id': loan.id,
                'invoice_type': 'loan',
                'amount': loan.net_loan_per_month,
                'status': 'pending',
                'created_at': datetime.now(),
                'created_by_id': None
            }

            InvoiceModel(invoiceInfo=params, name=loan.member.first_name)


generate_invoice()
