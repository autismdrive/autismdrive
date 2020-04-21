"""merge cf9f2ed356ab and 12b4edc6125b

Revision ID: 80c3b2f1d995
Revises: cf9f2ed356ab, 12b4edc6125b
Create Date: 2020-04-21 14:04:13.168702

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '80c3b2f1d995'
down_revision = ('cf9f2ed356ab', '12b4edc6125b')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
