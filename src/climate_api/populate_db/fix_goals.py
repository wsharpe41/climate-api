"""Fix an error with the goals column in the companies table"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from climate_api.internal.Company import Company


# Create a connection to the database
def connect_to_db() -> None:
    """Create a connection to the database

    Returns:
        None
    """
    # Create an engine to connect to the database
    # Get user variable pg_pass from environment
    pg_pass = os.environ.get("pg_pass")
    engine = create_engine(
        f"postgresql+psycopg2://postgres:{pg_pass}@localhost:5432/climate_api"
    )
    # Create a session to interact with the database
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


# Every row in the companies table has a goals column that is a foreign key to the goals table
# For each row decrease that goals column by 1
def fix_goals(session):
    """Decrement the goals column in the companies table by 1

    Args:
        session (sqlalchemy.orm.session.Session): Database session
    """
    # Get all companies from the companies table
    companies = session.query(Company).all()
    for company in companies:
        # Decrease the goal id by 1
        if company.goals:
            company.goals = company.goals - 1
            # Update the company in the companies table
            session.add(company)
    session.commit()


if __name__ == "__main__":
    db = connect_to_db()
    fix_goals(db)
