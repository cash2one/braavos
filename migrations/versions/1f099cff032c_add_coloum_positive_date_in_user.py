"""add coloum positive_date in user

Revision ID: 1f099cff032c
Revises: 424b76369e0f
Create Date: 2016-03-14 11:21:29.181931

"""

# revision identifiers, used by Alembic.
revision = '1f099cff032c'
down_revision = '424b76369e0f'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('positive_date', sa.DateTime(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'positive_date')
    ### end Alembic commands ###
