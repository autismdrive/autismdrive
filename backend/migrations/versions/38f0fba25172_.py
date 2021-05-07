"""empty message

Revision ID: 38f0fba25172
Revises: 122b7ade20c7
Create Date: 2021-05-07 13:17:48.943698

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '38f0fba25172'
down_revision = '122b7ade20c7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'usermeta', 'stardrive_user', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'usermeta', type_='foreignkey')
    # ### end Alembic commands ###
