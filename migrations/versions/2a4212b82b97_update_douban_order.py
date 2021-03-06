"""update douban order

Revision ID: 2a4212b82b97
Revises: 1c482661b4b1
Create Date: 2015-01-09 14:33:21.140309

"""

# revision identifiers, used by Alembic.
revision = '2a4212b82b97'
down_revision = '1c482661b4b1'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('douban_order_users_designerer',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('order_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['order_id'], ['bra_douban_order.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    op.create_table('douban_order_users_operater',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('order_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['order_id'], ['bra_douban_order.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    op.create_table('douban_order_users_planer',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('order_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['order_id'], ['bra_douban_order.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('douban_order_users_planer')
    op.drop_table('douban_order_users_operater')
    op.drop_table('douban_order_users_designerer')
    ### end Alembic commands ###
