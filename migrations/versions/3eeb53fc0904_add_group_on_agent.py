"""add group on agent

Revision ID: 3eeb53fc0904
Revises: 359f726bfd9f
Create Date: 2014-12-30 11:37:49.053861

"""

# revision identifiers, used by Alembic.
revision = '3eeb53fc0904'
down_revision = '359f726bfd9f'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('agent', sa.Column('group_id', sa.Integer(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('agent', 'group_id')
    ### end Alembic commands ###