"""added list cover images

Revision ID: 72ed8272aad3
Revises: c8d2ed28ad42
Create Date: 2023-10-10 14:05:51.255123

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "72ed8272aad3"
down_revision: Union[str, None] = "c8d2ed28ad42"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, "pictures", ["id"])
    op.create_unique_constraint(None, "ratings", ["id"])
    op.add_column(
        "restaurant_lists", sa.Column("cover_picture_id", sa.UUID(), nullable=True)
    )
    op.create_unique_constraint(None, "restaurant_lists", ["id"])
    op.create_foreign_key(
        None, "restaurant_lists", "pictures", ["cover_picture_id"], ["id"]
    )
    op.create_unique_constraint(None, "restaurants", ["id"])
    op.create_unique_constraint(None, "tags", ["id"])
    op.create_unique_constraint(None, "users", ["id"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("users_id_key", "users", type_="unique")
    op.drop_constraint("tags_id_key", "tags", type_="unique")
    op.drop_constraint("restaurants_id_key", "restaurants", type_="unique")
    op.drop_constraint(
        "restaurant_lists_cover_picture_id_fkey", "restaurant_lists", type_="foreignkey"
    )
    op.drop_constraint("restaurant_lists_id_key", "restaurant_lists", type_="unique")
    op.drop_column("restaurant_lists", "cover_picture_id")
    op.drop_constraint("ratings_id_key", "ratings", type_="unique")
    op.drop_constraint("pictures_id_key", "pictures", type_="unique")
    # ### end Alembic commands ###