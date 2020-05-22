"""Updated table

Revision ID: e0fd4c883760
Revises: 3d1dcd7d5daf
Create Date: 2020-05-20 19:02:15.124281

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e0fd4c883760'
down_revision = '3d1dcd7d5daf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('QA',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('question', sa.String(length=256), nullable=True),
    sa.Column('option1', sa.String(length=256), nullable=True),
    sa.Column('option2', sa.String(length=256), nullable=True),
    sa.Column('option3', sa.String(length=256), nullable=True),
    sa.Column('answer', sa.String(length=256), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_QA_answer'), 'QA', ['answer'], unique=False)
    op.create_index(op.f('ix_QA_option1'), 'QA', ['option1'], unique=False)
    op.create_index(op.f('ix_QA_option2'), 'QA', ['option2'], unique=False)
    op.create_index(op.f('ix_QA_option3'), 'QA', ['option3'], unique=False)
    op.create_index(op.f('ix_QA_question'), 'QA', ['question'], unique=False)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=64), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('score',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('score', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('score')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_QA_question'), table_name='QA')
    op.drop_index(op.f('ix_QA_option3'), table_name='QA')
    op.drop_index(op.f('ix_QA_option2'), table_name='QA')
    op.drop_index(op.f('ix_QA_option1'), table_name='QA')
    op.drop_index(op.f('ix_QA_answer'), table_name='QA')
    op.drop_table('QA')
    # ### end Alembic commands ###