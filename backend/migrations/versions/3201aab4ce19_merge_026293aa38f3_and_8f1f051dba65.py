"""merge 026293aa38f3 and 8f1f051dba65

Revision ID: 3201aab4ce19
Revises: 026293aa38f3, 8f1f051dba65
Create Date: 2019-02-15 13:13:29.500163

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3201aab4ce19'
down_revision = ('026293aa38f3', '8f1f051dba65')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
