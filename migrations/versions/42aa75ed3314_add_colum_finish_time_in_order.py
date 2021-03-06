"""add colum finish_time in order

Revision ID: 42aa75ed3314
Revises: 2e4ec4661d34
Create Date: 2015-09-06 16:14:58.789045

"""

# revision identifiers, used by Alembic.
revision = '42aa75ed3314'
down_revision = '2e4ec4661d34'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bra_client_order', sa.Column('finish_time', sa.DateTime(), nullable=True))
    op.add_column('bra_douban_order', sa.Column('finish_time', sa.DateTime(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('bra_douban_order', 'finish_time')
    op.drop_column('bra_client_order', 'finish_time')
    ### end Alembic commands ###
