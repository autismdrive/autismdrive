"""empty message

Revision ID: 2787d7772d4f
Revises: 8b0cb19f8e0d
Create Date: 2019-08-21 10:46:35.482722

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '2787d7772d4f'
down_revision = '8b0cb19f8e0d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('event', 'last_updated')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('event', sa.Column('last_updated', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
