from sqlalchemy.orm import Session
from contextvars import ContextVar

from .internal.Company import Company
from .internal.CompanyYear import CompanyYear
from .internal.Year import Year
from .internal.Goal import Goal

db_session: ContextVar[Session] = ContextVar("db_session")


def get_companies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Company).offset(skip).limit(limit).all()


def get_company(db: Session, company_name: int):
    return db.query(Company).filter(Company.title == company_name).first()


def get_company_year(db: Session, company_name: str, year: int):
    # From the company name get the id of the company
    # Then get the year objects that have relationships with that id from the company_year table
    # From those years return the year object that has the year that matches the year parameter
    company = db.query(Company).filter(Company.title == company_name).first()
    if not company:
        return None  # Return None if company doesn't exist

    company_years = (
        db.query(CompanyYear).filter(CompanyYear.company_id == company.id).all()
    )
    # Get the year_id for each company_year
    year_ids = [company_year.year_id for company_year in company_years]
    # Get the year objects for each year_id
    years = db.query(Year).filter(Year.id.in_(year_ids)).all()
    # Return the year object that matches the year parameter
    for year_obj in years:
        if year_obj.year == year:
            return year_obj
    return None


def get_company_years(db: Session, company_name: str):
    # From the company name get the id of the company
    # Then get the year objects that have relationships with that id from the company_year table
    # From those years return the year object that has the year that matches the year parameter
    company = db.query(Company).filter(Company.title == company_name).first()
    if not company:
        return None  # Return None if company doesn't exist
    company_years = (
        db.query(CompanyYear).filter(CompanyYear.company_id == company.id).all()
    )
    # Get the year_id for each company_year
    year_ids = [company_year.year_id for company_year in company_years]
    # Get the year objects for each year_id
    years = db.query(Year).filter(Year.id.in_(year_ids)).all()
    return years


# Given a goals id return that goal
def get_goal(db: Session, goal_id: int):
    return db.query(Goal).filter(Goal.id == goal_id).first()


# Given a year and a scope return the emissions for that year and scope
def get_emissions(db: Session, year: int, limit: int = 100):
    year_obj = db.query(Year).filter(Year.year == year).limit(limit).all()
    if not year_obj:
        return None
    return year_obj


def get_all_emissions(db: Session, skip: int = 0, limit: int = 100):
    years = db.query(Year).offset(skip).limit(limit).all()
    # For year in years 
    # If both scope1_2 and scope1_2_3 are None then remove that year from the list
    # Return the list of years
    filtered_years = []

    # Iterate over the years
    for year in years:
        # If either scope1_2 or scope1_2_3 is not None, keep the year
        if year.scope1_2 is not None or year.scope1_2_3 is not None:
            filtered_years.append(year)
    return filtered_years


def get_scope3_emissions(db: Session, year: int):
    # Get total emissions and subtract scope 1 and 2 emissions
    all_emission = get_emissions(db, year)
    scope_1_2_3 = 0.0
    for em in all_emission:
        if em.scope1_2_3 is not None and em.scope1_2 is not None:
            scope_1_2_3 += em.scope1_2_3 - em.scope1_2
    return scope_1_2_3