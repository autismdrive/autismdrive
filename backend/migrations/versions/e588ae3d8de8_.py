"""empty message

Revision ID: e588ae3d8de8
Revises: 204f00c31973
Create Date: 2019-02-19 10:01:00.746896

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'e588ae3d8de8'
down_revision = '204f00c31973'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('home_dependent_questionnaire',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('last_updated', sa.DateTime(), nullable=True),
    sa.Column('time_on_task_ms', sa.BigInteger(), nullable=True),
    sa.Column('participant_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('dependent_living_situation', sa.String(), nullable=True),
    sa.Column('dependent_living_other', sa.String(), nullable=True),
    sa.Column('struggle_to_afford', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['participant_id'], ['stardrive_participant.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['stardrive_user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('home_self_questionnaire',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('last_updated', sa.DateTime(), nullable=True),
    sa.Column('time_on_task_ms', sa.BigInteger(), nullable=True),
    sa.Column('participant_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('self_living_situation', sa.String(), nullable=True),
    sa.Column('self_living_other', sa.String(), nullable=True),
    sa.Column('struggle_to_afford', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['participant_id'], ['stardrive_participant.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['stardrive_user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_constraint('housemate_home_questionnaire_id_fkey', 'housemate', type_='foreignkey')
    op.drop_column('housemate', 'home_questionnaire_id')
    op.drop_table('home_questionnaire')
    op.add_column('housemate', sa.Column('home_dependent_questionnaire_id', sa.Integer(), nullable=True))
    op.add_column('housemate', sa.Column('home_self_questionnaire_id', sa.Integer(), nullable=True))
    op.create_foreign_key('housemate_home_dependent_questionnaire_id_fkey', 'housemate', 'home_dependent_questionnaire', ['home_dependent_questionnaire_id'], ['id'])
    op.create_foreign_key('housemate_home_self_questionnaire_id_fkey', 'housemate', 'home_self_questionnaire', ['home_self_questionnaire_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    op.create_table('home_questionnaire',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('last_updated', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('participant_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('self_living_situation', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('self_living_other', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('struggle_to_afford', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('dependent_living_other', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('dependent_living_situation', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('time_on_task_ms', sa.BIGINT(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['participant_id'], ['stardrive_participant.id'], name='home_questionnaire_participant_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['stardrive_user.id'], name='home_questionnaire_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='home_questionnaire_pkey')
    )

    op.add_column('housemate', sa.Column('home_questionnaire_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('housemate_home_questionnaire_id_fkey', 'housemate', 'home_questionnaire', ['home_questionnaire_id'], ['id'])

    op.drop_constraint('housemate_home_dependent_questionnaire_id_fkey', 'housemate', type_='foreignkey')
    op.drop_constraint('housemate_home_self_questionnaire_id_fkey', 'housemate', type_='foreignkey')
    op.drop_column('housemate', 'home_self_questionnaire_id')
    op.drop_column('housemate', 'home_dependent_questionnaire_id')
    op.drop_table('home_self_questionnaire')
    op.drop_table('home_dependent_questionnaire')
    # ### end Alembic commands ###
