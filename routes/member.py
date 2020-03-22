from flask import request, jsonify, make_response, current_app
from flask_restful import Resource, reqparse
from datetime import datetime
from uuid import uuid4

from internals.app import db
from internals.mailgun import send_simple_message
from internals.utils import token_required, decode_token, user_check
from models.users import Users as UserModel
from models.members import Members as MemberModel, member_schema
from models.beneficiaries import Beneficiaries as BeneficiariesModel
from models.shares import MemberShares as MemberSharesModel
from models.invoices import Invoices as InvoiceModel

from pathlib import Path


class Member(Resource):

    @token_required
    def get(self, uuid):
        member = MemberModel.query.filter_by(uuid=uuid).first()
        result = member_schema().dump(member)

        return make_response(result, 200)

    def post(self):
        app = current_app
        params = request.get_json(force=True)

        memberData = params.get('memberForm')

        email = memberData.get('email')
        del memberData['email']

        beneficiaries = None
        share = None
        if memberData.get('share'):
            share = memberData.get('share')
            del memberData['share']

        if memberData.get('beneficiaries'):
            beneficiaries = memberData.get('beneficiaries')
            del memberData['beneficiaries']

        params = {
            **memberData,
            'status': 'pending',
            'uuid': uuid4(),
            'created_at': datetime.now(),
            'created_by_id': None
        }

        try:
            isDuplicateInfo = MemberModel.query.filter(
                MemberModel.first_name == params.get('first_name')
            ).filter(
                MemberModel.last_name == params.get('last_name')
            ).filter(
                MemberModel.middle_name == params.get('middle_name')
            ).filter(
                MemberModel.dob == params.get('dob')
            ).first()

            if isDuplicateInfo is None:
                memberParams = MemberModel(**params)
                db.session.add(memberParams)
                db.session.commit()

                # Create member data
                userInfo = {
                    'uuid': uuid4(),
                    'email': email,
                    'password': 'placeholder',
                    'user_type': 'member',
                    'name': "%s" % (memberParams.first_name),
                    'member_id': memberParams.id,
                    'created_at': datetime.now(),
                    'status': 'disabled'
                }
                db.session.add(UserModel(**userInfo))
                db.session.commit()

                # Add any beneficiaries in the table
                if beneficiaries:
                    dbs = db.session
                    beneficiaryCommit = []
                    for beneficiary in beneficiaries:
                        benefitParams = {
                            **beneficiary,
                            'member_id': memberParams.id,
                            'created_at': datetime.now(),
                            'created_by_id': None
                        }
                        beneficiaryCommit.append(BeneficiariesModel(**benefitParams))
                    dbs.bulk_save_objects(beneficiaryCommit)
                    dbs.commit()

                if share:
                    # Rather than adding shares,
                    # create an invoice

                    amount = float(share['share_count']) * float(share['share_per_amount'])
                    print(share, 'share')
                    invoiceInfo = {
                        'uuid': uuid4(),
                        'invoice_type': 'shares',
                        'member_id': memberParams.id,
                        'status': 'pending',
                        'amount': amount
                    }
                    InvoiceModel()\
                        .createInvoice(
                            invoiceInfo=invoiceInfo,
                            name=memberParams.first_name)

                # Create an invoice for member registration
                invoiceInfo = {
                    'uuid': uuid4(),
                    'invoice_type': 'membership',
                    'member_id': memberParams.id,
                    'status': 'pending',
                    'amount': 250
                }
                InvoiceModel()\
                    .createInvoice(
                    invoiceInfo=invoiceInfo,
                    name=memberParams.first_name
                )

                # Send email confirming the registration
                previewUrl = "%s/member/preview/%s" \
                    % (app.config['FRONT_END_DOMAIN'], memberParams.uuid)

                approverUrl = "%s/member/%s" % (app.config['FRONT_END_DOMAIN'], memberParams.uuid)

                # For applicaiton member
                send_simple_message(
                    subject='Thank you for Registering',
                    text=Path('./templates/signup.template.html')
                    .read_text()
                    .replace("{{name}}", memberParams.first_name)
                    .replace("{{url}}", previewUrl)
                )

                # For Approver
                send_simple_message(
                    subject="%s wants to join our co-op" % (memberParams.first_name),
                    text=Path('./templates/forapproval.template.html')
                    .read_text()
                    .replace("{{name}}", "Approvers")
                    .replace("{{clientName}}", memberParams.first_name)
                    .replace("{{url}}", approverUrl)
                )

                return {'response': memberParams.uuid}
            return make_response({'error': 'Member is already registered'}, 500)
        except NameError as e:
            print(e)
            return make_response({'error': 'Something went wrong'}, 500)

    @token_required
    @user_check(user_type=['teller', 'approver'])
    def put(self, uuid):
        params = request.get_json(force=True)
        userInfo = decode_token()
        userType = userInfo.get('user_type')

        memberData = params.get('memberForm')
        if userType == 'teller':
            del memberData['shares']
            del memberData['loans']
            del memberData['created_at']

            forDeletion = params.get('forDeletion')
            beneficiaries = None
            share = None

            if memberData.get('share'):
                share = memberData.get('share')
                del memberData['share']

            if len(memberData.get('beneficiaries')) > 0:
                beneficiaries = memberData.get('beneficiaries')
                del memberData['beneficiaries']
            else:
                del memberData['beneficiaries']

        updateMemberData = {
            **memberData,
            'updated_at': datetime.now(),
            'updated_by_id': userInfo['id']
        }

        try:
            # Check if there are other member with the same set of details
            isDuplicateInfo = MemberModel\
                .query\
                .filter(MemberModel.uuid != uuid)\
                .filter(MemberModel.first_name == params.get('first_name'))\
                .filter(MemberModel.last_name == params.get('last_name'))\
                .filter(MemberModel.middle_name == params.get('middle_name'))\
                .filter(MemberModel.dob == params.get('dob'))\
                .first()

            if isDuplicateInfo is None:
                MemberModel\
                    .query\
                    .filter_by(uuid=uuid)\
                    .update(updateMemberData)

                memberInfo = MemberModel.query.filter_by(uuid=uuid).first()

                if userType == 'teller':
                    if beneficiaries:
                        memberInfo = MemberModel.query.filter_by(uuid=uuid).first()
                        dbs = db.session
                        forCreate = []
                        for beneficiary in beneficiaries:
                            if beneficiary.get('id'):
                                forUpdate = {
                                    **beneficiary,
                                    'updated_at': datetime.now(),
                                    'updated_by_id': userInfo['id']
                                }
                                del forUpdate['id']
                                BeneficiariesModel.query.filter_by(id=beneficiary.get('id')).update(forUpdate)
                            else:
                                benefitParams = {
                                    **beneficiary,
                                    'member_id': memberInfo.id,
                                    'created_at': datetime.now(),
                                    'created_by_id': userInfo['id']
                                }
                                forCreate.append(
                                    BeneficiariesModel(**benefitParams)
                                )
                        dbs.bulk_save_objects(forCreate)
                        dbs.commit()

                    if forDeletion:
                        dbs = db.session
                        for beneficiary in forDeletion:
                            BeneficiariesModel.query.filter_by(
                                id=beneficiary.get('id')
                            ).delete()
                        dbs.commit()

                    if share:
                        shareId = share.get('id')
                        del share['id']
                        MemberSharesModel.query.filter_by(id=shareId).update(share)
                        db.session.commit()

                # Send email to the user for the status

                if userType == 'approver':
                    status = updateMemberData['status']

                    send_simple_message(
                        subject="Your Appliation is %s" % (status),
                        text=Path('./templates/formStatus.template.html')
                        .read_text()
                        .replace("{{status}}", status)
                        .replace("{{name}}", memberInfo.first_name)
                    )

                    if status == 'approved':
                        # Approve User
                        UserModel\
                            .query\
                            .filter_by(member_id=memberInfo.id)\
                            .update({
                                'status': 'active',
                                'updated_at': datetime.now(),
                                'updated_by_id': userInfo['id']
                            })
                        UserModel()\
                            .createForgotPassword(email=memberInfo.userInfo.email)
                db.session.commit()

                return {'response': True}
            return make_response({'error': 'User is already made'}, 500)
        except Exception as e:
            print(e)
            return make_response({'error': 'Something is wrong'}, 500)


class MemberList(Resource):

    @token_required
    @user_check(user_type=['teller', 'approver', 'admin'])
    def get(self):
        try:
            membersQuery = MemberModel.query
            membersQuery = membersQuery\
                .order_by(
                    MemberModel.status.desc(),
                    MemberModel.updated_at.desc(),
                    MemberModel.created_at.desc()
                )\
                .all()
            result = member_schema(many=True, only=[
                "id",
                "uuid",
                "first_name",
                "last_name",
                "middle_name",
                "address",
                "contact_no",
                "status",
                "created_at",
                "updated_at"
            ]).dump(membersQuery)

            return {'response': result}
        except NameError:
            return make_response({'error': 'Something is wrong'}, 500)
