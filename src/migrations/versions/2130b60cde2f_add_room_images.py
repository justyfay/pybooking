"""add room images

Revision ID: 2130b60cde2f
Revises: 4d843b928465
Create Date: 2024-03-30 23:07:26.601482

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "2130b60cde2f"
down_revision: Union[str, None] = "4d843b928465"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("rooms", sa.Column("images", sa.JSON(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("rooms", "images")
    # ### end Alembic commands ###
