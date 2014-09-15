"""create all before tables

Revision ID: 2b831b35f37a
Revises: 289dfb84c199
Create Date: 2014-09-15 07:33:54.157792

"""

# revision identifiers, used by Alembic.
revision = '2b831b35f37a'
down_revision = '289dfb84c199'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ad_size',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('width', sa.Integer(), nullable=True),
    sa.Column('height', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('agent',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('team',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('type', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('client',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('industry', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('medium',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['team.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('pwdhash', sa.String(length=100), nullable=True),
    sa.Column('phone', sa.String(length=120), nullable=True),
    sa.Column('status', sa.Integer(), nullable=True),
    sa.Column('team_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['team_id'], ['team.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('phone')
    )
    op.create_table('bra_comment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('target_type', sa.String(length=50), nullable=True),
    sa.Column('target_id', sa.Integer(), nullable=True),
    sa.Column('msg', sa.String(length=1000), nullable=True),
    sa.Column('creator_id', sa.Integer(), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['creator_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ad_position',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('description', sa.String(length=500), nullable=True),
    sa.Column('size_id', sa.Integer(), nullable=True),
    sa.Column('status', sa.Integer(), nullable=True),
    sa.Column('level', sa.Integer(), nullable=True),
    sa.Column('medium_id', sa.Integer(), nullable=True),
    sa.Column('ad_type', sa.Integer(), nullable=True),
    sa.Column('cpd_num', sa.Integer(), nullable=True),
    sa.Column('max_order_num', sa.Integer(), nullable=True),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['medium_id'], ['medium.id'], ),
    sa.ForeignKeyConstraint(['size_id'], ['ad_size.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ad_unit',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('description', sa.String(length=500), nullable=True),
    sa.Column('size_id', sa.Integer(), nullable=True),
    sa.Column('margin', sa.String(length=50), nullable=True),
    sa.Column('target', sa.Integer(), nullable=True),
    sa.Column('status', sa.Integer(), nullable=True),
    sa.Column('medium_id', sa.Integer(), nullable=True),
    sa.Column('estimate_num', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['medium_id'], ['medium.id'], ),
    sa.ForeignKeyConstraint(['size_id'], ['ad_size.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('bra_order',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('client_id', sa.Integer(), nullable=True),
    sa.Column('campaign', sa.String(length=100), nullable=True),
    sa.Column('medium_id', sa.Integer(), nullable=True),
    sa.Column('order_type', sa.Integer(), nullable=True),
    sa.Column('contract', sa.String(length=100), nullable=True),
    sa.Column('money', sa.Integer(), nullable=True),
    sa.Column('agent_id', sa.Integer(), nullable=True),
    sa.Column('creator_id', sa.Integer(), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['agent_id'], ['agent.id'], ),
    sa.ForeignKeyConstraint(['client_id'], ['client.id'], ),
    sa.ForeignKeyConstraint(['creator_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['medium_id'], ['medium.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('order_agent_sales',
    sa.Column('agent_sale_id', sa.Integer(), nullable=True),
    sa.Column('order_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['agent_sale_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['order_id'], ['bra_order.id'], )
    )
    op.create_table('order_users_operater',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('order_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['order_id'], ['bra_order.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    op.create_table('bra_item',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=True),
    sa.Column('description', sa.String(length=500), nullable=True),
    sa.Column('sale_type', sa.Integer(), nullable=True),
    sa.Column('position_id', sa.Integer(), nullable=True),
    sa.Column('special_sale', sa.Boolean(), nullable=True),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.Column('ad_type', sa.Integer(), nullable=True),
    sa.Column('priority', sa.Integer(), nullable=True),
    sa.Column('speed', sa.Integer(), nullable=True),
    sa.Column('status', sa.Integer(), nullable=True),
    sa.Column('item_status', sa.Integer(), nullable=True),
    sa.Column('creator_id', sa.Integer(), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['creator_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['order_id'], ['bra_order.id'], ),
    sa.ForeignKeyConstraint(['position_id'], ['ad_position.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('order_users_designerer',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('order_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['order_id'], ['bra_order.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    op.create_table('order_users_planer',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('order_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['order_id'], ['bra_order.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    op.create_table('ad_position_unit',
    sa.Column('position_id', sa.Integer(), nullable=True),
    sa.Column('unit_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['position_id'], ['ad_position.id'], ),
    sa.ForeignKeyConstraint(['unit_id'], ['ad_unit.id'], )
    )
    op.create_table('order_direct_sales',
    sa.Column('sale_id', sa.Integer(), nullable=True),
    sa.Column('order_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['order_id'], ['bra_order.id'], ),
    sa.ForeignKeyConstraint(['sale_id'], ['user.id'], )
    )
    op.create_table('bra_schedule',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('item_id', sa.Integer(), nullable=True),
    sa.Column('num', sa.Integer(), nullable=True),
    sa.Column('date', sa.Date(), nullable=True),
    sa.Column('start', sa.Time(), nullable=True),
    sa.Column('end', sa.Time(), nullable=True),
    sa.ForeignKeyConstraint(['item_id'], ['bra_item.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('materials',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('type', sa.Integer(), nullable=True),
    sa.Column('item_id', sa.Integer(), nullable=True),
    sa.Column('code', sa.Text(), nullable=True),
    sa.Column('props', sa.PickleType(), nullable=True),
    sa.Column('status', sa.Integer(), nullable=True),
    sa.Column('creator_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['creator_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['item_id'], ['bra_item.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('materials')
    op.drop_table('bra_schedule')
    op.drop_table('order_direct_sales')
    op.drop_table('ad_position_unit')
    op.drop_table('order_users_planer')
    op.drop_table('order_users_designerer')
    op.drop_table('bra_item')
    op.drop_table('order_users_operater')
    op.drop_table('order_agent_sales')
    op.drop_table('bra_order')
    op.drop_table('ad_unit')
    op.drop_table('ad_position')
    op.drop_table('bra_comment')
    op.drop_table('user')
    op.drop_table('medium')
    op.drop_table('client')
    op.drop_table('team')
    op.drop_table('agent')
    op.drop_table('ad_size')
    ### end Alembic commands ###
