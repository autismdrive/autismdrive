"""empty message

Revision ID: fcd6c141f060
Revises: 0bdde178b75e
Create Date: 2020-08-21 15:57:35.342233

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'fcd6c141f060'
down_revision = '0bdde178b75e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('registration_questionnaire',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('last_updated', sa.DateTime(timezone=True), nullable=True),
    sa.Column('time_on_task_ms', sa.BigInteger(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('event_id', sa.Integer(), nullable=True),
    sa.Column('first_name', sa.String(), nullable=True),
    sa.Column('last_name', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('zip_code', sa.Integer(), nullable=True),
    sa.Column('relationship_to_autism', sa.ARRAY(sa.String()), nullable=True),
    sa.Column('relationship_other', sa.String(), nullable=True),
    sa.Column('marketing_channel', sa.ARRAY(sa.String()), nullable=True),
    sa.Column('marketing_other', sa.String(), nullable=True),
    sa.Column('newsletter_consent', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['event_id'], ['event.id'], name='registration_questionnaire_event_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['stardrive_user.id'], name='registration_questionnaire_user_id_fkey'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('registration_questionnaire')
    # ### end Alembic commands ###
