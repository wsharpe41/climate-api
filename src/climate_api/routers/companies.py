"""This module contains the FastAPI router for the companies endpoint."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..models import Company, Year, Goal
from .. import crud
from ..database import SessionLocal

router = APIRouter()


def get_db():
    """
    Get a database connection and close it after use
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_change(years: list, scope: str) -> float:
    """
    For years find the change in emissions from the most recent year to the oldest year

    Args:
        years (list): All years for a company
        scope (str): Emissions scope to compare

    Returns:
        float: Absolute change in emissions
    """
    if len(years) < 2:
        return 0, 0

    earliest, latest = None, None

    for yr in years:
        val = getattr(yr, scope)
        if val is not None:
            if earliest is None:
                earliest = val
            latest = val

    if earliest is None or latest is None:
        return 0, 0

    return latest, earliest


@router.get("/companies", tags=["companies"], response_model=list[Company])
async def get_companies_list(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """
    Query companies table in database and return list of companies
    Args:
        skip (int, optional): Amount of results to skip. Defaults to 0.
        limit (int, optional): Limit on results #. Defaults to 100.
        db (Session, optional): Database session. Defaults to Depends(get_db).

    Returns:
        list: List of comapny objects
    """
    return crud.get_companies(db=db, skip=skip, limit=limit)


@router.get("/companies/{company}", tags=["companies"], response_model=Company)
async def get_company(company: str, db: Session = Depends(get_db)):
    """
    Get a company by name

    Args:
        company (str): Company Name
        db (Session, optional): DB session. Defaults to Depends(get_db).

    Raises:
        HTTPException: 404 if company not found

    Returns:
        Company: Company object
    """
    company = crud.get_company(db=db, company_name=company)
    if company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    return company


@router.get(
    "/companies/{company}/all_years", tags=["companies"], response_model=list[Year]
)
async def get_all_company_data(company: str, db: Session = Depends(get_db)):
    """
    Get all years of data for a company

    Args:
        company (str): Company Name
        db (Session, optional): DB session. Defaults to Depends(get_db).

    Raises:
        HTTPException: 404 if company not found

    Returns:
        list[Year]: List of Year objects
    """
    company_data = crud.get_company_years(db=db, company_name=company)
    if company_data is None:
        raise HTTPException(status_code=404, detail="Company not found")
    return company_data


@router.get("/companies/{company}/change_1_2", tags=["companies"], response_model=float)
async def get_company_change_1_2(
    company: str, db: Session = Depends(get_db), percent: bool = False
):
    """
    Get the change in emissions for a company from the most recent year to the oldest year
    Args:
        company (str): Company Name
        db (Session, optional): DB session. Defaults to Depends(get_db).
        percent (bool, optional): If you want percent or absolute change. Defaults to False.

    Raises:
        HTTPException: _description_
        HTTPException: _description_

    Returns:
        float: Absolute or percent change in emissions
    """
    years = crud.get_company_years(db=db, company_name=company)
    if years is None:
        raise HTTPException(
            status_code=404, detail=f"No data found for {company} not found"
        )
    e, s = get_change(years, "scope1_2")
    if e == 0 or s == 0:
        raise HTTPException(
            status_code=404, detail=f"No change data found for {company} not found"
        )
    if percent:
        return 100 * (e - s) / s
    return e - s


@router.get(
    "/companies/{company}/change_1_2_3", tags=["companies"], response_model=float
)
async def get_company_change_1_2_3(
    company: str, db: Session = Depends(get_db), percent: bool = False
):
    """
    Get the change in all emissions for a company from the most recent year to the oldest year

    Args:
        company (str): Company Name
        db (Session, optional): DB session. Defaults to Depends(get_db).
        percent (bool, optional): Whether or not to return percent change Defaults to False.

    Raises:
        HTTPException: 404 if company not found
        HTTPException: 404 if no change data found

    Returns:
        float: Absolute or percent change in emissions
    """

    years = crud.get_company_years(db=db, company_name=company)
    if years is None:
        raise HTTPException(
            status_code=404, detail=f"No data found for {company} not found"
        )

    e, s = get_change(years, "scope1_2_3")
    if e == 0 or s == 0:
        raise HTTPException(
            status_code=404, detail=f"No change data found for {company} not found"
        )
    if percent:
        return 100 * (e - s) / s
    return e - s


@router.get(
    "/companies/{company}/change_1_2/{start}_{end}",
    tags=["companies"],
    response_model=float,
)
async def get_company_change_with_years_1_2(
    company: str,
    start: int,
    end: int,
    db: Session = Depends(get_db),
    percent: bool = False,
):
    """
    Get the change in emissions for a company between two years

    Args:
        company (str): Company Name
        start (int): Start year
        end (int): End year
        db (Session, optional): DB session. Defaults to Depends(get_db).
        percent (bool, optional): Whether or not to return percent change. Defaults to False.

    Raises:
        HTTPException: 404 if company not found
        HTTPException: 404 if no data found for start or end year

    Returns:
        float: Absolute or percent change in emissions
    """
    start = crud.get_company_year(db, company, start)
    end = crud.get_company_year(db, company, end)
    if start.scope1_2 is None:
        raise HTTPException(
            status_code=404,
            detail=f"No data found for {company} for year {start} not found",
        )
    if end.scope1_2 is None:
        raise HTTPException(
            status_code=404,
            detail=f"No data found for {company} for year {end} not found",
        )
    if percent:
        return 100 * (end.scope1_2 - start.scope1_2) / start.scope1_2
    else:
        return end.scope1_2 - start.scope1_2


@router.get(
    "/companies/{company}/change_1_2_3/{start}_{end}",
    tags=["companies"],
    response_model=float,
)
async def get_company_change_with_years_1_2_3(
    company: str,
    start: int,
    end: int,
    db: Session = Depends(get_db),
    percent: bool = False,
):
    """
    Get the change in all emissions for a company between two years

    Args:
        company (str): Company Name
        start (int): Start year
        end (int): End year
        db (Session, optional): DB session. Defaults to Depends(get_db).
        percent (bool, optional): Whether or not to return percent change. Defaults to False.

    Raises:
        HTTPException: 404 if company not found
        HTTPException: 404 if no data found for start or end year

    Returns:
        float: Absolute or percent change in emissions
    """
    start = crud.get_company_year(db, company, start)
    end = crud.get_company_year(db, company, end)
    if start.scope1_2_3 is None:
        raise HTTPException(
            status_code=404,
            detail=f"No data found for {company} for year {start} not found",
        )
    if end.scope1_2_3 is None:
        raise HTTPException(
            status_code=404,
            detail=f"No data found for {company} for year {end} not found",
        )
    if percent:
        return 100 * (end.scope1_2_3 - start.scope1_2_3) / start.scope1_2_3
    return end.scope1_2_3 - start.scope1_2_3


@router.get("/companies/{company}/goals", tags=["companies"], response_model=Goal)
async def get_company_goals(company: str, db: Session = Depends(get_db)):
    """
    Get the goals for a company

    Args:
        company (str): Company Name
        db (Session, optional): DB Session. Defaults to Depends(get_db).

    Raises:
        HTTPException: 404 if company not found
        HTTPException: 404 if no goals found for company

    Returns:
        Goal: Goal object
    """
    comp = crud.get_company(db, company)
    if comp is None:
        raise HTTPException(status_code=404, detail="Company not found")
    goal = crud.get_goal(db, comp.goals)
    if goal is None:
        raise HTTPException(status_code=404, detail=f"No goals for {company} found")
    return goal


@router.get("/companies/{company}/{year}", tags=["companies"], response_model=Year)
async def get_company_year(company: str, year: int, db: Session = Depends(get_db)):
    """
    Get a specific year of data for a company

    Args:
        company (str): Company Name
        year (int): Year
        db (Session, optional): DB session. Defaults to Depends(get_db).

    Raises:
        HTTPException: 404 if company not found for year

    Returns:
        Year: Year object
    """
    year = crud.get_company_year(db=db, company_name=company, year=year)
    if year is None:
        raise HTTPException(
            status_code=404,
            detail=f"No data found for {company} for year {year} not found",
        )
    return year
