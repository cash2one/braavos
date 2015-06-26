"""add new Model AgentRebate MediumRebate AgentInvoice AgentInvoicePay

Revision ID: 3ed998b96ab8
Revises: 8352e011c85
Create Date: 2015-06-26 16:08:48.993835

"""

# revision identifiers, used by Alembic.
revision = '3ed998b96ab8'
down_revision = '8352e011c85'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bra_medium_rebate',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('medium_id', sa.Integer(), nullable=True),
    sa.Column('rebate', sa.Float(), nullable=True),
    sa.Column('year', sa.Date(), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['medium_id'], ['medium.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('medium_id', 'year', name='_medium_rebate_year')
    )
    op.create_table('bra_agent_rebate',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('agent_id', sa.Integer(), nullable=True),
    sa.Column('inad_rebate', sa.Float(), nullable=True),
    sa.Column('douban_rebate', sa.Float(), nullable=True),
    sa.Column('year', sa.Date(), nullable=True),
    sa.Column('creator_id', sa.Integer(), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['agent_id'], ['agent.id'], ),
    sa.ForeignKeyConstraint(['creator_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('agent_id', 'year', name='_agent_rebate_year')
    )
    op.create_table('bra_agent_invoice',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('client_order_id', sa.Integer(), nullable=True),
    sa.Column('agent_id', sa.Integer(), nullable=True),
    sa.Column('company', sa.String(length=100), nullable=True),
    sa.Column('tax_id', sa.String(length=100), nullable=True),
    sa.Column('address', sa.String(length=120), nullable=True),
    sa.Column('phone', sa.String(length=80), nullable=True),
    sa.Column('bank_id', sa.String(length=20), nullable=True),
    sa.Column('bank', sa.String(length=100), nullable=True),
    sa.Column('detail', sa.String(length=200), nullable=True),
    sa.Column('money', sa.Float(), nullable=True),
    sa.Column('pay_money', sa.Float(), nullable=True),
    sa.Column('invoice_type', sa.Integer(), nullable=True),
    sa.Column('invoice_status', sa.Integer(), nullable=True),
    sa.Column('invoice_num', sa.String(length=200), nullable=True),
    sa.Column('creator_id', sa.Integer(), nullable=True),
    sa.Column('add_time', sa.DateTime(), nullable=True),
    sa.Column('pay_time', sa.DateTime(), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('bool_pay', sa.Boolean(), nullable=True),
    sa.Column('bool_invoice', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['agent_id'], ['agent.id'], ),
    sa.ForeignKeyConstraint(['client_order_id'], ['bra_client_order.id'], ),
    sa.ForeignKeyConstraint(['creator_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('bra_agent_invoice_pay',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('agent_invoice_id', sa.Integer(), nullable=True),
    sa.Column('detail', sa.String(length=200), nullable=True),
    sa.Column('pay_status', sa.Integer(), nullable=True),
    sa.Column('money', sa.Float(), nullable=True),
    sa.Column('pay_time', sa.DateTime(), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['agent_invoice_id'], ['bra_agent_invoice.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('bra_agent_invoice_pay')
    op.drop_table('bra_agent_invoice')
    op.drop_table('bra_agent_rebate')
    op.drop_table('bra_medium_rebate')
    ### end Alembic commands ###
