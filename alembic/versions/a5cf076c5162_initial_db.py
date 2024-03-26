"""initial_db

Revision ID: a5cf076c5162
Revises: 
Create Date: 2024-03-18 21:23:17.401104

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "a5cf076c5162"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create years table
    op.create_table(
        "years",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("year", sa.Integer, nullable=False),
        sa.Column("scope1_2", sa.Float, nullable=False),
        sa.Column("scope3", sa.Float, nullable=False),
    )

    # Create companies table

    # Create goals table
    op.create_table(
        "goals",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("scope12_target_year", sa.Integer, nullable=False),
        sa.Column("scope12_percent_decrease", sa.Float, nullable=False),
        sa.Column("scope3_target_year", sa.Integer, nullable=False),
        sa.Column("scope3_percent_decrease", sa.Float, nullable=False),
        sa.Column("scope_12_reference_year", sa.Integer, nullable=False),
        sa.Column("scope_3_reference_year", sa.Integer, nullable=False),
    )

    op.create_table(
        "companies",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("description", sa.String(255), nullable=True),
        sa.Column("report_link", sa.String(255), nullable=True),
        sa.Column("goals", sa.Integer, sa.ForeignKey("goals.id"), nullable=True),
    )

    # Create table for one-to-many relationship between companies and years
    op.create_table(
        "company_years",
        sa.Column(
            "company_id", sa.Integer, sa.ForeignKey("companies.id"), nullable=False
        ),
        sa.Column("year_id", sa.Integer, sa.ForeignKey("years.id"), nullable=False),
    )


def downgrade() -> None:
    # Drop all tables
    op.drop_table("company_years")
    op.drop_table("companies")
    op.drop_table("goals")
    op.drop_table("years")
