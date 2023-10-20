"""empty message

Revision ID: c9c9f11655f4
Revises: 
Create Date: 2018-12-05 10:39:22.469335

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "c9c9f11655f4"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "resource",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=True),
        sa.Column("last_updated", sa.DateTime(), nullable=True),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("image", sa.String(), nullable=True),
        sa.Column("image_caption", sa.String(), nullable=True),
        sa.Column("organization", sa.String(), nullable=True),
        sa.Column("street_address1", sa.String(), nullable=True),
        sa.Column("street_address2", sa.String(), nullable=True),
        sa.Column("city", sa.String(), nullable=True),
        sa.Column("state", sa.String(), nullable=True),
        sa.Column("zip", sa.String(), nullable=True),
        sa.Column("county", sa.String(), nullable=True),
        sa.Column("phone", sa.String(), nullable=True),
        sa.Column("website", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "study",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=True),
        sa.Column("last_updated", sa.DateTime(), nullable=True),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("researcher_description", sa.String(), nullable=True),
        sa.Column("participant_description", sa.String(), nullable=True),
        sa.Column("outcomes", sa.String(), nullable=True),
        sa.Column("enrollment_date", sa.DateTime(), nullable=True),
        sa.Column("current_enrolled", sa.Integer(), nullable=True),
        sa.Column("total_participants", sa.Integer(), nullable=True),
        sa.Column("study_start", sa.DateTime(), nullable=True),
        sa.Column("study_end", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "training",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=True),
        sa.Column("last_updated", sa.DateTime(), nullable=True),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("outcomes", sa.String(), nullable=True),
        sa.Column("image", sa.String(), nullable=True),
        sa.Column("image_caption", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("last_updated", sa.DateTime(), nullable=True),
        sa.Column("first_name", sa.String(), nullable=True),
        sa.Column("last_name", sa.String(), nullable=True),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.LargeBinary(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("user")
    op.drop_table("training")
    op.drop_table("study")
    op.drop_table("resource")
    # ### end Alembic commands ###
