"""add group

Revision ID: 359f726bfd9f
Revises: 50009ec44238
Create Date: 2014-12-30 11:12:15.698255

"""

# revision identifiers, used by Alembic.
revision = '359f726bfd9f'
down_revision = '50009ec44238'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bra_group',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('bra_group')
    ### end Alembic commands ###
