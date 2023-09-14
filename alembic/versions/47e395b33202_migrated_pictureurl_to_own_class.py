"""migrated pictureUrl to own class

Revision ID: 47e395b33202
Revises: 2aa6d0f5dff5
Create Date: 2023-09-08 20:27:32.319121

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '47e395b33202'
down_revision: Union[str, None] = '2aa6d0f5dff5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('pictures', sa.Column('created_at', sa.String(), nullable=True))
    op.add_column('pictures', sa.Column('pictureURL', sa.String(), nullable=True))
    op.drop_constraint('pictures_owner_id_fkey', 'pictures', type_='foreignkey')
    op.drop_constraint('pictures_rating_id_fkey', 'pictures', type_='foreignkey')
    op.drop_column('pictures', 'rating_id')
    op.drop_column('pictures', 'picture')
    op.drop_column('pictures', 'owner_id')
    op.drop_column('ratings', 'pictureURL')
    op.alter_column('tags', 'name',
               existing_type=sa.VARCHAR(length=50),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('tags', 'name',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)
    op.add_column('ratings', sa.Column('pictureURL', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('pictures', sa.Column('owner_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('pictures', sa.Column('picture', postgresql.BYTEA(), autoincrement=False, nullable=True))
    op.add_column('pictures', sa.Column('rating_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('pictures_rating_id_fkey', 'pictures', 'ratings', ['rating_id'], ['id'])
    op.create_foreign_key('pictures_owner_id_fkey', 'pictures', 'users', ['owner_id'], ['id'])
    op.drop_column('pictures', 'pictureURL')
    op.drop_column('pictures', 'created_at')
    # ### end Alembic commands ###