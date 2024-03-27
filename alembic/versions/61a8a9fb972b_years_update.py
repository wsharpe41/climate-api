"""years_update

Revision ID: 61a8a9fb972b
Revises: a5cf076c5162
Create Date: 2024-03-20 18:27:34.264411

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = "61a8a9fb972b"
down_revision = "a5cf076c5162"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # In years table change the scope3 column to be called scope1_2_3
    with op.batch_alter_table("years") as batch_op:
        batch_op.alter_column("scope3",
                              new_column_name="scope1_2_3",
                              nullable=True)

    # Make the scope1_2_3 and scope1_2 columns nullable
    with op.batch_alter_table("years") as batch_op:
        batch_op.alter_column("scope1_2_3", nullable=True)
        batch_op.alter_column("scope1_2", nullable=True)


def downgrade() -> None:
    # Undo the changes made in the upgrade
    with op.batch_alter_table("years") as batch_op:
        batch_op.alter_column("scope1_2_3",
                              new_column_name="scope3",
                              nullable=False)

    # Make the scope1_2_3 and scope1_2 columns non-nullable
    with op.batch_alter_table("years") as batch_op:
        batch_op.alter_column("scope1_2_3", nullable=False)
        batch_op.alter_column("scope1_2", nullable=False)
