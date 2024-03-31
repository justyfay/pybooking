"""change column images json

Revision ID: 9db87f144afb
Revises: f18718391a84
Create Date: 2024-03-30 22:13:12.873191

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "9db87f144afb"
down_revision: Union[str, None] = "f18718391a84"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("hotels", sa.Column("images", sa.JSON(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("hotels", "images")
    # ### end Alembic commands ###
