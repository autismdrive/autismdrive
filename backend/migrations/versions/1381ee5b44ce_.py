"""empty message

Revision ID: 1381ee5b44ce
Revises: 694e37e7d38a
Create Date: 2019-09-20 13:06:56.837556

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1381ee5b44ce'
down_revision = '694e37e7d38a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admin_note',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('resource_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('last_updated', sa.DateTime(timezone=True), nullable=True),
    sa.Column('note', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['resource_id'], ['resource.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['stardrive_user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('admin_note')
    # ### end Alembic commands ###