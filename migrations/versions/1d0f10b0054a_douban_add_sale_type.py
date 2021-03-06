"""douban add sale type

Revision ID: 1d0f10b0054a
Revises: 3f0b1b1b898
Create Date: 2015-01-13 18:29:11.294597

"""

# revision identifiers, used by Alembic.
revision = '1d0f10b0054a'
down_revision = '3f0b1b1b898'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bra_client_order', sa.Column('sale_type', sa.Integer(), nullable=True))
    op.add_column('bra_douban_order', sa.Column('sale_type', sa.Integer(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('bra_douban_order', 'sale_type')
    op.drop_column('bra_client_order', 'sale_type')
    ### end Alembic commands ###
