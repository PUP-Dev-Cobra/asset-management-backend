"""add add params for freeze values loans

Revision ID: b4eef12a45ba
Revises: 20e9d00e2d58
Create Date: 2020-01-30 19:07:43.352869

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b4eef12a45ba'
down_revision = '20e9d00e2d58'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('loans', sa.Column('loan_payment_start_date', sa.Date(), nullable=False))
    op.add_column('loans', sa.Column('share_amount', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('loans', 'share_amount')
    op.drop_column('loans', 'loan_payment_start_date')
    # ### end Alembic commands ###