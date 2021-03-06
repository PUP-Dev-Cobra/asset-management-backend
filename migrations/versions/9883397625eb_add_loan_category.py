"""add loan category

Revision ID: 9883397625eb
Revises: 85a77779c175
Create Date: 2020-03-08 15:38:15.155297

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9883397625eb'
down_revision = '85a77779c175'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('loans', sa.Column('loan_category', sa.String(), nullable=True))
    op.drop_column('loans', 'loan_payment_start_date')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('loans', sa.Column('loan_payment_start_date', sa.DATE(), autoincrement=False, nullable=False))
    op.drop_column('loans', 'loan_category')
    # ### end Alembic commands ###
