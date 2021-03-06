"""add table medium

Revision ID: 103fe6b97f9b
Revises: 3deed38a65c3
Create Date: 2015-06-15 11:38:49.194169

"""

# revision identifiers, used by Alembic.
revision = '103fe6b97f9b'
down_revision = '3deed38a65c3'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bra_medium_resource',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('medium_id', sa.Integer(), nullable=True),
    sa.Column('type', sa.Integer(), nullable=True),
    sa.Column('number', sa.String(), nullable=True),
    sa.Column('shape', sa.Integer(), nullable=True),
    sa.Column('product', sa.Integer(), nullable=True),
    sa.Column('resource_type', sa.Integer(), nullable=True),
    sa.Column('page_postion', sa.String(length=200), nullable=True),
    sa.Column('ad_position', sa.String(length=200), nullable=True),
    sa.Column('cpm', sa.Float(), nullable=True),
    sa.Column('b_click', sa.Integer(), nullable=True),
    sa.Column('click_rate', sa.Float(), nullable=True),
    sa.Column('buy_unit', sa.Integer(), nullable=True),
    sa.Column('buy_threshold', sa.String(length=200), nullable=True),
    sa.Column('money', sa.Float(), nullable=True),
    sa.Column('b_directional', sa.Integer(), nullable=True),
    sa.Column('directional_type', sa.Integer(), nullable=True),
    sa.Column('directional_money', sa.Float(), nullable=True),
    sa.Column('discount', sa.Float(), nullable=True),
    sa.Column('ad_size', sa.String(length=200), nullable=True),
    sa.Column('materiel_format', sa.String(length=200), nullable=True),
    sa.Column('less_buy', sa.Integer(), nullable=True),
    sa.Column('b_give', sa.Integer(), nullable=True),
    sa.Column('give_desc', sa.String(length=200), nullable=True),
    sa.Column('b_check_exposure', sa.Integer(), nullable=True),
    sa.Column('b_check_click', sa.Integer(), nullable=True),
    sa.Column('b_out_link', sa.Integer(), nullable=True),
    sa.Column('b_in_link', sa.Integer(), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('update_time', sa.DateTime(), nullable=True),
    sa.Column('body', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['medium_id'], ['medium.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('bra_medium_product_app',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('medium_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('update_time', sa.DateTime(), nullable=True),
    sa.Column('install_count', sa.Integer(), nullable=True),
    sa.Column('activation_count', sa.Integer(), nullable=True),
    sa.Column('register_count', sa.Integer(), nullable=True),
    sa.Column('active_count_by_day', sa.Integer(), nullable=True),
    sa.Column('active_count_by_month', sa.Integer(), nullable=True),
    sa.Column('pv_by_day', sa.Integer(), nullable=True),
    sa.Column('pv_by_month', sa.Integer(), nullable=True),
    sa.Column('open_rate_by_day', sa.Float(), nullable=True),
    sa.Column('access_time', sa.Float(), nullable=True),
    sa.Column('sex_distributed', sa.String(length=255), nullable=True),
    sa.Column('age_distributed', sa.String(length=255), nullable=True),
    sa.Column('area_distributed', sa.String(length=255), nullable=True),
    sa.Column('education_distributed', sa.String(length=255), nullable=True),
    sa.Column('income_distributed', sa.String(length=255), nullable=True),
    sa.Column('ugc_count', sa.Integer(), nullable=True),
    sa.Column('cooperation_type', sa.Integer(), nullable=True),
    sa.Column('divide_into', sa.Float(), nullable=True),
    sa.Column('policies', sa.Float(), nullable=True),
    sa.Column('delivery', sa.String(length=255), nullable=True),
    sa.Column('special', sa.String(length=255), nullable=True),
    sa.Column('product_position', sa.String(length=255), nullable=True),
    sa.Column('body', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['medium_id'], ['medium.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('medium_id', 'name', name='_medium_product_app_id_name_unique')
    )
    op.create_table('bra_medium_product_pc',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('medium_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('update_time', sa.DateTime(), nullable=True),
    sa.Column('register_count', sa.Integer(), nullable=True),
    sa.Column('alone_count_by_day', sa.Integer(), nullable=True),
    sa.Column('active_count_by_day', sa.Integer(), nullable=True),
    sa.Column('alone_count_by_month', sa.Integer(), nullable=True),
    sa.Column('active_count_by_month', sa.Integer(), nullable=True),
    sa.Column('pv_by_day', sa.Integer(), nullable=True),
    sa.Column('pv_by_month', sa.Integer(), nullable=True),
    sa.Column('access_time', sa.Integer(), nullable=True),
    sa.Column('ugc_count', sa.Integer(), nullable=True),
    sa.Column('cooperation_type', sa.Integer(), nullable=True),
    sa.Column('divide_into', sa.Float(), nullable=True),
    sa.Column('policies', sa.Float(), nullable=True),
    sa.Column('delivery', sa.String(length=255), nullable=True),
    sa.Column('special', sa.String(length=255), nullable=True),
    sa.Column('sex_distributed', sa.String(length=255), nullable=True),
    sa.Column('age_distributed', sa.String(length=255), nullable=True),
    sa.Column('area_distributed', sa.String(length=255), nullable=True),
    sa.Column('education_distributed', sa.String(length=255), nullable=True),
    sa.Column('income_distributed', sa.String(length=255), nullable=True),
    sa.Column('product_position', sa.String(length=255), nullable=True),
    sa.Column('body', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['medium_id'], ['medium.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('medium_id', 'name', name='_medium_product_pc_id_name_unique')
    )
    op.create_table('bra_medium_product_down',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('medium_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('update_time', sa.DateTime(), nullable=True),
    sa.Column('start_time', sa.DateTime(), nullable=True),
    sa.Column('end_time', sa.DateTime(), nullable=True),
    sa.Column('location', sa.String(length=100), nullable=True),
    sa.Column('subject', sa.String(length=255), nullable=True),
    sa.Column('before_year_count', sa.Integer(), nullable=True),
    sa.Column('now_year_count', sa.Integer(), nullable=True),
    sa.Column('sex_distributed', sa.String(length=255), nullable=True),
    sa.Column('age_distributed', sa.String(length=255), nullable=True),
    sa.Column('area_distributed', sa.String(length=255), nullable=True),
    sa.Column('education_distributed', sa.String(length=255), nullable=True),
    sa.Column('income_distributed', sa.String(length=255), nullable=True),
    sa.Column('cooperation_type', sa.Integer(), nullable=True),
    sa.Column('divide_into', sa.Float(), nullable=True),
    sa.Column('policies', sa.Float(), nullable=True),
    sa.Column('delivery', sa.String(length=255), nullable=True),
    sa.Column('special', sa.String(length=255), nullable=True),
    sa.Column('product_position', sa.String(length=255), nullable=True),
    sa.Column('business_start_time', sa.DateTime(), nullable=True),
    sa.Column('business_end_time', sa.DateTime(), nullable=True),
    sa.Column('body', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['medium_id'], ['medium.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('medium_id', 'name', name='_medium_product_down_id_name_unique')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('bra_medium_product_down')
    op.drop_table('bra_medium_product_pc')
    op.drop_table('bra_medium_product_app')
    op.drop_table('bra_medium_resource')
    ### end Alembic commands ###
