"""create posts table

Revision ID: f6b4aef120b1
Revises: 
Create Date: 2023-01-05 10:09:54.354696

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f6b4aef120b1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("posts", sa.Column('id', sa.Integer(), nullable=False, primary_key=True), sa.Column('title', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_table("posts")
