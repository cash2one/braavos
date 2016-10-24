"""add colum in okr

Revision ID: 3ab8bad72e5b
Revises: 24f0b264b5bd
Create Date: 2016-10-17 17:49:23.389264

"""

# revision identifiers, used by Alembic.
revision = '3ab8bad72e5b'
down_revision = '24f0b264b5bd'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_okr', sa.Column('score_colleague', sa.Text(), nullable=True))
    op.add_column('user_okr', sa.Column('score_kpi', sa.Float(), nullable=True))
    op.add_column('user_okr', sa.Column('score_leader', sa.Text(), nullable=True))
    op.add_column('user_okr', sa.Column('score_okr', sa.Float(), nullable=True))
    op.drop_column('user_okr', 'score')
    op.drop_column('user_okr', 'c_score')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_okr', sa.Column('c_score', sa.TEXT(), autoincrement=False, nullable=True))
    op.add_column('user_okr', sa.Column('score', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_column('user_okr', 'score_okr')
    op.drop_column('user_okr', 'score_leader')
    op.drop_column('user_okr', 'score_kpi')
    op.drop_column('user_okr', 'score_colleague')
    ### end Alembic commands ###