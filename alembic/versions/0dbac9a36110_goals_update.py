"""'goals_update'

Revision ID: 0dbac9a36110
Revises: 61a8a9fb972b
Create Date: 2024-03-20 18:45:04.113138

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0dbac9a36110'
down_revision = '61a8a9fb972b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Remove the scope_12_reference_year column and the scope_3_reference_year column from the goals table
    with op.batch_alter_table("goals") as batch_op:
        batch_op.drop_column("scope_12_reference_year")
        batch_op.drop_column("scope_3_reference_year")
    # Add a reference_year column to the goals table
    op.add_column("goals", sa.Column("reference_year", sa.Integer, nullable=False))
    # Make every column nullable besided the id column
    with op.batch_alter_table("goals") as batch_op:
        batch_op.alter_column("scope12_target_year", nullable=True)
        batch_op.alter_column("scope12_percent_decrease", nullable=True)
        batch_op.alter_column("scope3_target_year", nullable=True)
        batch_op.alter_column("scope3_percent_decrease", nullable=True)
        batch_op.alter_column("reference_year", nullable=True)
    

def downgrade() -> None:
    # Remove the reference_year column from the goals table
    with op.batch_alter_table("goals") as batch_op:
        batch_op.drop_column("reference_year")
    # Add the scope_12_reference_year column and the scope_3_reference_year column to the goals table
    with op.batch_alter_table("goals") as batch_op:
        batch_op.add_column(sa.Column("scope_12_reference_year", sa.Integer, nullable=False))
        batch_op.add_column(sa.Column("scope_3_reference_year", sa.Integer, nullable=False))
    # Make every column non-nullable
    with op.batch_alter_table("goals") as batch_op:
        batch_op.alter_column("scope12_target_year", nullable=False)
        batch_op.alter_column("scope12_percent_decrease", nullable=False)
        batch_op.alter_column("scope3_target_year", nullable=False)
        batch_op.alter_column("scope3_percent_decrease", nullable=False)
        batch_op.alter_column("reference_year", nullable=False)