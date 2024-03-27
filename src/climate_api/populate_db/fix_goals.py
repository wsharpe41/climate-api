"""Fix an error with the goals column in the companies table"""
from climate_api.internal.Company import Company
from climate_api.populate_db.populate_db import connect_to_db


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
