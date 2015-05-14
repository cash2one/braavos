"""add table medium_invoice_pay

Revision ID: 4e86dc3c8dd1
Revises: 3f778837a66f
Create Date: 2015-05-13 16:34:08.831550

"""

# revision identifiers, used by Alembic.
revision = '4e86dc3c8dd1'
down_revision = '3f778837a66f'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bra_medium_invoice_pay',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('medium_invoice_id', sa.Integer(), nullable=True),
    sa.Column('detail', sa.String(length=200), nullable=True),
    sa.Column('pay_status', sa.Integer(), nullable=True),
    sa.Column('money', sa.Float(), nullable=True),
    sa.Column('pay_time', sa.DateTime(), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['medium_invoice_id'], ['bra_medium_invoice.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('mail')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('mail',
    sa.Column('id', sa.INTEGER(), server_default="nextval('mail_id_seq'::regclass)", nullable=False),
    sa.Column('recipients', sa.VARCHAR(length=1000), autoincrement=False, nullable=True),
    sa.Column('subject', sa.VARCHAR(length=1000), autoincrement=False, nullable=True),
    sa.Column('body', sa.VARCHAR(length=1000), autoincrement=False, nullable=True),
    sa.Column('files', sa.VARCHAR(length=1000), autoincrement=False, nullable=True),
    sa.Column('remark', sa.VARCHAR(length=1000), autoincrement=False, nullable=True),
    sa.Column('creator_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('create_time', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['creator_id'], [u'user.id'], name=u'mail_creator_id_fkey'),
    sa.PrimaryKeyConstraint('id', name=u'mail_pkey')
    )
    op.drop_table('bra_medium_invoice_pay')
    ### end Alembic commands ###