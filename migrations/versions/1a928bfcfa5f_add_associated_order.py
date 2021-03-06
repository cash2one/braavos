"""add associated order

Revision ID: 1a928bfcfa5f
Revises: 2a4212b82b97
Create Date: 2015-01-10 20:07:11.578287

"""

# revision identifiers, used by Alembic.
revision = '1a928bfcfa5f'
down_revision = '2a4212b82b97'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bra_associated_douban_order',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('medium_order_id', sa.Integer(), nullable=True),
    sa.Column('contract', sa.String(length=100), nullable=True),
    sa.Column('creator_id', sa.Integer(), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['creator_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['medium_order_id'], ['bra_order.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('bra_associated_douban_order')
    ### end Alembic commands ###
