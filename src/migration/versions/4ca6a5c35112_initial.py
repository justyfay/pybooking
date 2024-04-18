"""initial

Revision ID: 4ca6a5c35112
Revises:
Create Date: 2024-04-16 18:44:51.856034

"""

from pathlib import Path
from typing import Sequence, Union

from alembic import op
from sqlalchemy import text

revision: str = "4ca6a5c35112"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    dump_path = Path(__file__).parent.parent.absolute() / "migration.dump"

    with open(dump_path) as sql_reader:
        op.execute(text(sql_reader.read()))

    op.execute(text("SET search_path = public"))


def downgrade() -> None:
    pass
