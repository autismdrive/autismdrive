"""merge 38cb1825439a and 1dbc5d6304d8

Revision ID: 9496baebe784
Revises: 38cb1825439a, 1dbc5d6304d8
Create Date: 2019-03-08 16:22:52.416529

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9496baebe784'
down_revision = ('38cb1825439a', '1dbc5d6304d8')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
