"""merge f543f7586a61 and 6238def0a892

Revision ID: 590fafb9db61
Revises: f543f7586a61, 6238def0a892
Create Date: 2019-06-24 11:57:26.750762

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '590fafb9db61'
down_revision = ('f543f7586a61', '6238def0a892')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
