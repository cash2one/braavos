"""add colum framework

Revision ID: 143bade867cc
Revises: 4738e8321b11
Create Date: 2014-12-17 15:37:32.709896

"""

# revision identifiers, used by Alembic.
revision = '143bade867cc'
down_revision = '4738e8321b11'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('agent', sa.Column('framework', sa.String(length=100), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('agent', 'framework')
    ### end Alembic commands ###
