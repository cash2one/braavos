"""add msg channel on comments

Revision ID: 257ca960c779
Revises: 993b80c198c
Create Date: 2015-03-20 12:27:39.437505

"""

# revision identifiers, used by Alembic.
revision = '257ca960c779'
down_revision = '993b80c198c'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bra_comment', sa.Column('msg_channel', sa.Integer(), default=0, nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('bra_comment', 'msg_channel')
    ### end Alembic commands ###
