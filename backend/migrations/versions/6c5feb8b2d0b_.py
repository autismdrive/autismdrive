"""empty message

Revision ID: 6c5feb8b2d0b
Revises: 9b14a3e90c8e
Create Date: 2020-12-18 11:49:43.961774

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '6c5feb8b2d0b'
down_revision = '9b14a3e90c8e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('chain_step',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('instruction', sa.String(), nullable=True),
    sa.Column('last_updated', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('chain_questionnaire',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('last_updated', sa.DateTime(timezone=True), nullable=True),
    sa.Column('time_on_task_ms', sa.BigInteger(), nullable=True),
    sa.Column('participant_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['participant_id'], ['stardrive_participant.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['stardrive_user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('chain_session',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('last_updated', sa.DateTime(timezone=True), nullable=True),
    sa.Column('time_on_task_ms', sa.BigInteger(), nullable=True),
    sa.Column('chain_questionnaire_id', sa.Integer(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('completed', sa.Boolean(), nullable=True),
    sa.Column('session_type', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['chain_questionnaire_id'], ['chain_questionnaire.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('chain_session_step',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('last_updated', sa.DateTime(timezone=True), nullable=True),
    sa.Column('chain_session_id', sa.Integer(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('status', sa.String(), nullable=True),
    sa.Column('completed', sa.Boolean(), nullable=True),
    sa.Column('was_prompted', sa.Boolean(), nullable=True),
    sa.Column('prompt_level', sa.String(), nullable=True),
    sa.Column('had_challenging_behavior', sa.Boolean(), nullable=True),
    sa.Column('challenging_behavior_severity', sa.String(), nullable=True),
    sa.Column('chain_step_id', sa.Integer(), nullable=True),
    sa.Column('participant_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['chain_session_id'], ['chain_session.id'], ),
    sa.ForeignKeyConstraint(['chain_step_id'], ['chain_step.id'], ),
    sa.ForeignKeyConstraint(['participant_id'], ['stardrive_participant.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['stardrive_user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('chain_session_step')
    op.drop_table('chain_session')
    op.drop_table('chain_questionnaire')
    op.drop_table('chain_step')
    # ### end Alembic commands ###