"""added picture url column to ratings

Revision ID: 8543568717ad
Revises: 94f6a37fb5dd
Create Date: 2023-09-01 02:56:50.020123

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8543568717ad'
down_revision: Union[str, None] = '94f6a37fb5dd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ratings', sa.Column('pictureURL', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('ratings', 'pictureURL')
    # ### end Alembic commands ###
