"""add colum in okr

Revision ID: adf1d898998
Revises: 136dd738c2dd
Create Date: 2016-10-10 16:32:54.495314

"""

# revision identifiers, used by Alembic.
revision = 'adf1d898998'
down_revision = '136dd738c2dd'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    ### op.drop_column('searchad_bra_client_order_bill', 'invoice_apply_sum')
    ### op.drop_column('searchad_bra_client_order_bill', 'invoice_pass_sum')
    op.add_column('user_okr', sa.Column('comment', sa.Text(), nullable=True))
    op.add_column('user_okr', sa.Column('score', sa.Integer(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_okr', 'score')
    op.drop_column('user_okr', 'comment')
    ### op.add_column('searchad_bra_client_order_bill', sa.Column('invoice_pass_sum', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))
    ### op.add_column('searchad_bra_client_order_bill', sa.Column('invoice_apply_sum', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))
    ### end Alembic commands ###