from fastapi import APIRouter, Depends, HTTPException
from ..models import Company, Year, Goal
from .. import crud
from sqlalchemy.orm import Session
from ..database import SessionLocal

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_change(years: list, scope: str) -> float:
    # For years find the change in emissions from the most recent year to the oldest year
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


@router.get("/companies", tags=["companies"])
async def get_companies_list(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    # Query companies table in database and return list of companies
    return crud.get_companies(db=db, skip=skip, limit=limit)


@router.get("/companies/{company}", tags=["companies"], response_model=Company)
async def get_company(company: str, db: Session = Depends(get_db)):
    # Return company object
    company = crud.get_company(db=db, company_name=company)
    # Return 404 if company not found
    if company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    return company


@router.get(
    "/companies/{company}/all_years", tags=["companies"], response_model=list[Year]
)
async def get_all_company_data(company: str, db: Session = Depends(get_db)):
    # Return company object
    company_data = crud.get_company_years(db=db, company_name=company)
    if company_data is None:
        raise HTTPException(status_code=404, detail="Company not found")
    return company_data


@router.get("/companies/{company}/change_1_2", tags=["companies"], response_model=float)
async def get_company_change_1_2(company: str, db: Session = Depends(get_db),percent: bool = False):
    # get_crompany_year from
    years = crud.get_company_years(db=db, company_name=company)
    if years is None:
        raise HTTPException(
            status_code=404, detail=f"No data found for {company} not found"
        )
    # For years find the change in emissions from the most recent year to the oldest year
    e, s = get_change(years, "scope1_2")
    if e == 0 or s == 0:
        raise HTTPException(
            status_code=404, detail=f"No change data found for {company} not found"
        )
    if percent:
        return 100 * (e - s) / s
    else:
        return e - s


@router.get(
    "/companies/{company}/change_1_2_3", tags=["companies"], response_model=float
)
async def get_company_change_1_2_3(company: str, db: Session = Depends(get_db),percent: bool = False):
    # get_crompany_year from
    years = crud.get_company_years(db=db, company_name=company)
    if years is None:
        raise HTTPException(
            status_code=404, detail=f"No data found for {company} not found"
        )
    # For years find the change in emissions from the most recent year to the oldest year
    e, s = get_change(years, "scope1_2_3")
    if e == 0 or s == 0:
        raise HTTPException(
            status_code=404, detail=f"No change data found for {company} not found"
        )
    if percent:
        return 100 * (e - s) / s
    else:
        return e - s


@router.get(
    "/companies/{company}/change_1_2/{start}_{end}",
    tags=["companies"],
    response_model=float,
)
async def get_company_change_with_years_1_2(
    company: str, start: int, end: int, db: Session = Depends(get_db), percent: bool = False
):
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
    company: str, start: int, end: int, db: Session = Depends(get_db), percent: bool = False
):
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
    else:
        return end.scope1_2_3 - start.scope1_2_3


@router.get("/companies/{company}/goals", tags=["companies"], response_model=Goal)
async def get_company_goals(company: str, db: Session = Depends(get_db)):
    comp = crud.get_company(db, company)
    if comp is None:
        raise HTTPException(status_code=404, detail="Company not found")
    goal = crud.get_goal(db, comp.goals)
    if goal is None:
        raise HTTPException(status_code=404, detail=f"No goals for {company} found")
    return goal


@router.get("/companies/{company}/{year}", tags=["companies"], response_model=Year)
async def get_company_year(company: str, year: int, db: Session = Depends(get_db)):
    year = crud.get_company_year(db=db, company_name=company, year=year)
    if year is None:
        raise HTTPException(
            status_code=404,
            detail=f"No data found for {company} for year {year} not found",
        )
    return year
