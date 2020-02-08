"""rename disbursment table

Revision ID: 071a47a0da41
Revises: 6ac4d30b7563
Create Date: 2020-02-02 16:54:51.920092

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '071a47a0da41'
down_revision = '6ac4d30b7563'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('disbursments',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('uuid', sa.String(length=100), nullable=False),
    sa.Column('loan_id', sa.Integer(), nullable=False),
    sa.Column('check_voucher', sa.String(), nullable=False),
    sa.Column('check_number', sa.String(), nullable=False),
    sa.Column('created_at', sa.DATETIME(), nullable=False),
    sa.Column('updated_at', sa.DATETIME(), nullable=True),
    sa.Column('created_by_id', sa.Integer(), nullable=False),
    sa.Column('updated_by_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['created_by_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['loan_id'], ['loans.id'], ),
    sa.ForeignKeyConstraint(['updated_by_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('uuid')
    )
    op.drop_table('disbursment')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('disbursment',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False, mssql_identity_start=1, mssql_identity_increment=1),
    sa.Column('uuid', sa.VARCHAR(length=100, collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=False),
    sa.Column('loan_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('check_voucher', sa.VARCHAR(collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=False),
    sa.Column('check_number', sa.VARCHAR(collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=False),
    sa.Column('created_at', sa.DATETIME(), autoincrement=False, nullable=False),
    sa.Column('updated_at', sa.DATETIME(), autoincrement=False, nullable=True),
    sa.Column('created_by_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('updated_by_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['created_by_id'], ['users.id'], name='FK__disbursme__creat__3E1D39E1'),
    sa.ForeignKeyConstraint(['loan_id'], ['loans.id'], name='FK__disbursme__loan___4D5F7D71'),
    sa.ForeignKeyConstraint(['updated_by_id'], ['users.id'], name='FK__disbursme__updat__3F115E1A'),
    sa.PrimaryKeyConstraint('id', name='PK__disbursm__3213E83F9520CB42')
    )
    op.drop_table('disbursments')
    # ### end Alembic commands ###
