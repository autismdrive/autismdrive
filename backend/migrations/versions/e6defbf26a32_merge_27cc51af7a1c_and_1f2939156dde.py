"""merge 27cc51af7a1c and 1f2939156dde

Revision ID: e6defbf26a32
Revises: 27cc51af7a1c, 1f2939156dde
Create Date: 2019-09-09 13:46:51.770526

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e6defbf26a32'
down_revision = ('27cc51af7a1c', '1f2939156dde')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
