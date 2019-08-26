"""merge 8b0cb19f8e0d and 26887885bf9c

Revision ID: e8692e08942d
Revises: 8b0cb19f8e0d, 26887885bf9c
Create Date: 2019-08-26 16:24:46.206589

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e8692e08942d'
down_revision = ('8b0cb19f8e0d', '26887885bf9c')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
