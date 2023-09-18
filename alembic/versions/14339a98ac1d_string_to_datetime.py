"""string to datetime

Revision ID: 14339a98ac1d
Revises: b57174d005db
Create Date: 2023-09-18 13:22:46.059909

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '14339a98ac1d'
down_revision: Union[str, None] = 'b57174d005db'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # change column type from String to DateTime
    op.execute("ALTER TABLE ratings ALTER COLUMN created_at TYPE TIMESTAMP USING created_at::timestamp without time zone")
    op.execute("ALTER TABLE pictures ALTER COLUMN created_at TYPE TIMESTAMP USING created_at::timestamp without time zone")


def downgrade() -> None:
    # reverse the change if needed to downgrade the database
    op.execute("ALTER TABLE ratings ALTER COLUMN created_at TYPE VARCHAR USING created_at::varchar")
    op.execute("ALTER TABLE pictures ALTER COLUMN created_at TYPE VARCHAR USING created_at::varchar")
