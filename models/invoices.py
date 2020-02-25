from internals.app import db
from datetime import datetime
from pathlib import Path
import locale

from internals.mailgun import send_simple_message
from schemas.invoices import InvoiceSchema


class Invoices(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
        unique=True
    )
    uuid = db.Column(
        db.String(100),
        nullable=False,
        unique=True
    )
    member_id = db.Column(
        db.Integer,
        db.ForeignKey('members.id'),
        nullable=False
    )
    loan_id = db.Column(
        db.Integer,
        db.ForeignKey('loans.id'),
        nullable=True
    )
    invoice_type = db.Column(
        db.String,
        nullable=False
    )
    amount = db.Column(
        db.Float,
        nullable=False
    )
    status = db.Column(
        db.String,
        nullable=False
    )
    created_at = db.Column(
        db.DATETIME,
        nullable=False
    )
    updated_at = db.Column(
        db.DATETIME,
        nullable=True
    )
    created_by_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=True
    )
    updated_by_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=True
    )

    def createInvoice(self, invoiceInfo, name):
        try:
            invoiceInfo = {
                **invoiceInfo,
                'created_at': datetime.now()
            }

            invoiceModel = Invoices(**invoiceInfo)
            db.session.add(invoiceModel)
            db.session.commit()

            send_simple_message(
                subject='Your Invoice For %s' % (invoiceInfo['invoice_type']),
                text=Path('./templates/invoice.template.html')
                .read_text()
                .replace("{{name}}", name)
                .replace("{{type}}", invoiceInfo['invoice_type'])
                .replace("{{amount}}", locale.format('%.2f', invoiceInfo['amount'], grouping=True))
            )

            return True
        except NameError as e:
            print(e)
            return False

    def voidInvoice(self, uuid, invoiceInfo, params, name):
        try:
            self\
                .query\
                .filter_by(uuid=uuid)\
                .update(invoiceInfo)

            send_simple_message(
                subject='Your Invoice For %s is Voided' % (params['invoice_type']),
                text=Path('./templates/void.invoice.template.html')
                .read_text()
                .replace("{{name}}", name)
                .replace("{{type}}", params['invoice_type'])
                .replace("{{amount}}", locale.format('%.2f', params['amount'], grouping=True))
            )

            db.session.commit()

        except NameError as e:
            print(e)
            return False


def invoice_schema(many=False, **kwargs):
    return InvoiceSchema(many=many, **kwargs)
