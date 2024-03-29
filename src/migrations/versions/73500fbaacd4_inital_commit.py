"""Inital commit

Revision ID: 73500fbaacd4
Revises:
Create Date: 2024-01-07 17:50:54.438572

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "73500fbaacd4"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "hotels",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("city_id", sa.Integer(), nullable=False),
        sa.Column("location", sa.String(), nullable=False),
        sa.Column("stars", sa.Integer(), nullable=False),
        sa.Column("amenities", sa.JSON(), nullable=False),
        sa.Column("rooms_quantity", sa.Integer(), nullable=False),
        sa.Column("image_id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("hashed_password", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "rooms",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("hotel_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("price", sa.Integer(), nullable=False),
        sa.Column("room_amenities", sa.JSON(), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("image_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["hotel_id"],
            ["hotels.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "bookings",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("room_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("date_from", sa.Date(), nullable=False),
        sa.Column("date_to", sa.Date(), nullable=False),
        sa.Column("price", sa.Integer(), nullable=False),
        sa.Column(
            "total_cost",
            sa.Integer(),
            sa.Computed(
                "(date_to - date_from) * price",
            ),
            nullable=False,
        ),
        sa.Column(
            "total_days",
            sa.Integer(),
            sa.Computed(
                "date_to - date_from",
            ),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["room_id"],
            ["rooms.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.alter_column(
        "city",
        "id",
        existing_type=sa.BIGINT(),
        type_=sa.Integer(),
        existing_nullable=False,
        autoincrement=True,
    )
    op.alter_column(
        "city",
        "region_id",
        existing_type=sa.BIGINT(),
        type_=sa.Integer(),
        existing_nullable=False,
    )
    op.alter_column(
        "city",
        "created_at",
        existing_type=postgresql.TIMESTAMP(timezone=True),
        type_=sa.TIMESTAMP(),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
    )
    op.alter_column(
        "country",
        "id",
        existing_type=sa.BIGINT(),
        type_=sa.Integer(),
        existing_nullable=False,
        autoincrement=True,
    )
    op.alter_column(
        "country",
        "created_at",
        existing_type=postgresql.TIMESTAMP(timezone=True),
        type_=sa.TIMESTAMP(),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
    )
    op.alter_column(
        "region",
        "id",
        existing_type=sa.BIGINT(),
        type_=sa.Integer(),
        existing_nullable=False,
        autoincrement=True,
    )
    op.alter_column(
        "region",
        "country_id",
        existing_type=sa.BIGINT(),
        type_=sa.Integer(),
        existing_nullable=False,
    )
    op.alter_column(
        "region",
        "created_at",
        existing_type=postgresql.TIMESTAMP(timezone=True),
        type_=sa.TIMESTAMP(),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "region",
        "created_at",
        existing_type=sa.TIMESTAMP(),
        type_=postgresql.TIMESTAMP(timezone=True),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
    )
    op.alter_column(
        "region",
        "country_id",
        existing_type=sa.Integer(),
        type_=sa.BIGINT(),
        existing_nullable=False,
    )
    op.alter_column(
        "region",
        "id",
        existing_type=sa.Integer(),
        type_=sa.BIGINT(),
        existing_nullable=False,
        autoincrement=True,
    )
    op.alter_column(
        "country",
        "created_at",
        existing_type=sa.TIMESTAMP(),
        type_=postgresql.TIMESTAMP(timezone=True),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
    )
    op.alter_column(
        "country",
        "id",
        existing_type=sa.Integer(),
        type_=sa.BIGINT(),
        existing_nullable=False,
        autoincrement=True,
    )
    op.alter_column(
        "city",
        "created_at",
        existing_type=sa.TIMESTAMP(),
        type_=postgresql.TIMESTAMP(timezone=True),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
    )
    op.alter_column(
        "city",
        "region_id",
        existing_type=sa.Integer(),
        type_=sa.BIGINT(),
        existing_nullable=False,
    )
    op.alter_column(
        "city",
        "id",
        existing_type=sa.Integer(),
        type_=sa.BIGINT(),
        existing_nullable=False,
        autoincrement=True,
    )
    op.drop_table("bookings")
    op.drop_table("rooms")
    op.drop_table("users")
    op.drop_table("hotels")
    # ### end Alembic commands ###
