"""empty message

Revision ID: 5fb917adc751
Revises: 704f78a74e54
Create Date: 2019-03-07 10:27:08.092311

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '5fb917adc751'
down_revision = '704f78a74e54'
branch_labels = None
depends_on = None

old_options = ('self_participant', 'self_guardian', 'dependent')
new_options = sorted(old_options + ('self_professional',))

old_type = sa.Enum(*old_options, name='relationship')
new_type = sa.Enum(*new_options, name='relationship')
tmp_type = sa.Enum(*new_options, name='_relationship')


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # Create a tempoary "_status" type, convert and drop the "old" type
    tmp_type.create(op.get_bind(), checkfirst=False)
    op.alter_column('stardrive_participant', 'relationship',
               existing_type=postgresql.ENUM('self_participant', 'self_guardian', 'dependent', name='relationship'),
               type_=sa.Enum('self_participant', 'self_guardian', 'dependent', 'self_professional', name='_relationship'),
               existing_nullable=True, postgresql_using="relationship::text::_relationship")
    old_type.drop(op.get_bind(), checkfirst=False)
    # Create and convert to the "new" status type
    new_type.create(op.get_bind(), checkfirst=False)
    op.alter_column('stardrive_participant', 'relationship',
               existing_type=postgresql.ENUM('self_participant', 'self_guardian', 'dependent', 'self_professional', name='_relationship'),
               type_=sa.Enum('self_participant', 'self_guardian', 'dependent', 'self_professional', name='relationship'),
               existing_nullable=True, postgresql_using="relationship::text::relationship")
    tmp_type.drop(op.get_bind(), checkfirst=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # Create a tempoary "_relationship" type, convert and drop the "new" type
    tmp_type.create(op.get_bind(), checkfirst=False)
    op.alter_column('stardrive_participant', 'relationship',
               existing_type=sa.Enum('self_participant', 'self_guardian', 'dependent', 'self_professional', name='relationship'),
               type_=postgresql.ENUM('self_participant', 'self_guardian', 'dependent', 'self_professional', name='_relationship'),
               existing_nullable=True, postgresql_using="relationship::text::_relationship")
    new_type.drop(op.get_bind(), checkfirst=False)
    # Create and convert to the "old" relationship type
    old_type.create(op.get_bind(), checkfirst=False)
    op.alter_column('stardrive_participant', 'relationship',
               existing_type=sa.Enum('self_participant', 'self_guardian', 'dependent', 'self_professional', name='_relationship'),
               type_=postgresql.ENUM('self_participant', 'self_guardian', 'dependent', name='relationship'),
               existing_nullable=True, postgresql_using="relationship::text::relationship")
    tmp_type.drop(op.get_bind(), checkfirst=False)
    # ### end Alembic commands ###
