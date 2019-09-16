"""merge bc81c8285922 and 974db61e6508

Revision ID: 694e37e7d38a
Revises: bc81c8285922, 974db61e6508
Create Date: 2019-09-16 14:26:14.886026

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '694e37e7d38a'
down_revision = ('bc81c8285922', '974db61e6508')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
