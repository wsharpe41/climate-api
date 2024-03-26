from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from climate_api.internal.Company import Company
from climate_api.internal.Goal import Goal


def connect_to_db() -> None:
    Base = declarative_base()
    # Create an engine to connect to the database
    engine = create_engine("sqlite:///S:\PycharmProjects\climate-api\climate-api.db")
    # Create a session to interact with the database
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


# Every row in the companies table has a goals column that is a foreign key to the goals table
# For each row decrease that goals column by 1
def fix_goals(session) -> None:
    # Get all companies from the companies table
    companies = session.query(Company).all()
    for company in companies:
        # Decrease the goal id by 1
        if company.goals:
            company.goals = company.goals - 1
            # Update the company in the companies table
            session.add(company)
    session.commit()
    return


if __name__ == "__main__":
    db = connect_to_db()
    fix_goals(db)
