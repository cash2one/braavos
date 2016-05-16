"""add table user_okr

Revision ID: 58cb643766b7
Revises: 56e4b905ebac
Create Date: 2016-05-16 10:04:47.154748

"""

# revision identifiers, used by Alembic.
revision = '58cb643766b7'
down_revision = '56e4b905ebac'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_okr',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('year', sa.Integer(), nullable=True),
    sa.Column('quarter', sa.Integer(), nullable=True),
    sa.Column('o_kr', sa.Text(), nullable=True),
    sa.Column('status', sa.Integer(), nullable=True),
    sa.Column('creator_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['creator_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_okr')
    ### end Alembic commands ###
