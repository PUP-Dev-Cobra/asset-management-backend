from flask import request, jsonify, make_response
from flask_restful import Resource, reqparse
from datetime import datetime
from uuid import uuid4

from internals.app import db
from internals.utils import token_required, decode_token, user_check
from models.members import Members as MemberModel, member_schema
from models.beneficiaries import Beneficiaries as BeneficiariesModel
from models.shares import MemberShares as MemberSharesModel


class Member(Resource):

    @token_required
    def get(self, uuid):
        member = MemberModel.query.filter_by(uuid=uuid).first()
        result = member_schema().dump(member)

        return make_response(result, 200)

    @token_required
    @user_check(user_type=['teller'])
    def post(self):
        params = request.get_json(force=True)
        memberInfo = decode_token()

        memberData = params.get('memberForm')
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
            'uuid': uuid4(),
            'created_at': datetime.now(),
            'created_by_id': memberInfo['id']
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

                # Add any beneficiaries in the table
                if beneficiaries:
                    dbs = db.session
                    beneficiaryCommit = []
                    for beneficiary in beneficiaries:
                        benefitParams = {
                            **beneficiary,
                            'member_id': memberParams.id,
                            'created_at': datetime.now(),
                            'created_by_id': memberInfo['id']
                        }
                        beneficiaryCommit.append(BeneficiariesModel(**benefitParams))
                    dbs.bulk_save_objects(beneficiaryCommit)
                    dbs.commit()

                if share:
                    newShareParams = {
                        **share,
                        'member_id': memberParams.id,
                        'created_at': datetime.now(),
                        'created_by_id': memberInfo['id']

                    }
                    newShare = MemberSharesModel(**newShareParams)
                    db.session.add(newShare)
                    db.session.commit()

                return {'response': memberParams.uuid}
            return make_response({'error': 'Member is already registered'}, 500)
        except Exception as e:
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
                db.session.commit()

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
