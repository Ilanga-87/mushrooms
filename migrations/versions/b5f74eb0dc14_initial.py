"""'initial'

Revision ID: b5f74eb0dc14
Revises: 
Create Date: 2024-11-27 05:18:30.527628

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b5f74eb0dc14'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'baskets',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('owner', sa.String, nullable=False),
        sa.Column('capacity', sa.Float, nullable=False),
    )

    op.create_table(
        'mushrooms',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('is_edible', sa.Boolean, nullable=False),
        sa.Column('weight', sa.Float, nullable=False),
        sa.Column('freshness', sa.Boolean, nullable=False),
        sa.Column('basket_id',
                  sa.Integer,
                  sa.ForeignKey('baskets.id', ondelete="SET NULL"),
                  nullable=True
        ),
    )

def downgrade() -> None:
    op.drop_table('mushrooms')
    op.drop_table('baskets')