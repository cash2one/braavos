"""add birthday for user table

Revision ID: 31661e578296
Revises: 3f111b604d89
Create Date: 2015-08-14 15:44:55.302667

"""

# revision identifiers, used by Alembic.
revision = '31661e578296'
down_revision = '3f111b604d89'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('birthday', sa.DateTime(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'birthday')
    ### end Alembic commands ###
