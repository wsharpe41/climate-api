"""CRUD operations for the database"""

from contextvars import ContextVar
from sqlalchemy.orm import Session

from .internal.Company import Company
from .internal.CompanyYear import CompanyYear
from .internal.Year import Year
from .internal.Goal import Goal

db_session: ContextVar[Session] = ContextVar("db_session")


def get_companies(db: Session, skip: int = 0, limit: int = 100) -> list[Company]:
    """Get all companies in the database

    Args:
        db (Session): SQLAlchemy session
        skip (int, optional): How many results to skip. Defaults to 0.
        limit (int, optional): Max amount of results to return. Defaults to 100.

    Returns:
        list[Company]: List of all companies
    """
    return db.query(Company).offset(skip).limit(limit).all()


def get_company(db: Session, company_name: str) -> Company:
    """Get a company by name

    Args:
        db (Session): SQLAlchemy session
        company_name (str): Name of the company to get

    Returns:
        Company: Company object that matches the company_name
    """
    return db.query(Company).filter(Company.title == company_name).first()


def get_company_year(db: Session, company_name: str, year: int) -> Year:
    """Get emissions for a given year and company

    Args:
        db (Session): SQLAlchemy session
        company_name (str): Name of the company to extract the year from
        year (int): Year to extract

    Returns:
        Year: Year object that matches the year parameter and company_name
    """
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


def get_company_years(db: Session, company_name: str) -> list[Year]:
    """For the company with the given name, get all the years

    Args:
        db (Session): SQLAlchemy session
        company_name (str): The name of the company to get years for

    Returns:
        list[Year]: Year objects that have relationships with the given company
    """
    company = db.query(Company).filter(Company.title == company_name).first()
    if not company:
        return None
    company_years = (
        db.query(CompanyYear).filter(CompanyYear.company_id == company.id).all()
    )
    # Get the year_id for each company_year
    year_ids = [company_year.year_id for company_year in company_years]
    # Get the year objects for each year_id
    years = db.query(Year).filter(Year.id.in_(year_ids)).all()
    return years


def get_goal(db: Session, goal_id: int) -> Goal:
    """Given a goals id return that goal

    Args:
        db (Session): SQLAlchemy session
        goal_id (int): The id of the goal to get

    Returns:
        Goal: The goal with the given id
    """
    return db.query(Goal).filter(Goal.id == goal_id).first()


def get_emissions(db: Session, year: int, limit: int = 100) -> list[Year]:
    """Given a year and a scope return the emissions for that year and scope

    Args:
        db (Session): SQLAlchemy session
        year (int): The year to get emissions for
        limit (int, optional): Max return amount. Defaults to 100.

    Returns:
        list[Year]: List of years with emissions for the given year
    """
    year_obj = db.query(Year).filter(Year.year == year).limit(limit).all()
    if not year_obj:
        return None
    return year_obj


def get_all_emissions(db: Session, skip: int = 0, limit: int = 100) -> list[Year]:
    """Get all years with emissions for every company

    Args:
        db (Session): SQLAlchemy session
        skip (int, optional): How many results to skip Defaults to 0.
        limit (int, optional): Max return amount. Defaults to 100.

    Returns:
        list[Year]: All years with emissions
    """

    years = db.query(Year).offset(skip).limit(limit).all()
    filtered_years = []

    # Iterate over the years
    for year in years:
        # If either scope1_2 or scope1_2_3 is not None, keep the year
        if year.scope1_2 is not None or year.scope1_2_3 is not None:
            filtered_years.append(year)
    return filtered_years


def get_scope3_emissions(db: Session, year: int) -> float:
    """Get only scope 3 emissions for a given year

    Args:
        db (Session): SQLAlchemy session
        year (int): The year to get emissions for

    Returns:
        float: The scope 3 emissions for the given year
    """
    all_emission = get_emissions(db, year)
    scope_1_2_3 = 0.0
    for emission in all_emission:
        if emission.scope1_2_3 is not None and emission.scope1_2 is not None:
            scope_1_2_3 += emission.scope1_2_3 - emission.scope1_2
    return scope_1_2_3
