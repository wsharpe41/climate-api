""" This module contains the routers for the years endpoint. """

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from ..database import SessionLocal
from .. import crud
from ..models import Year

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


@router.get("/year", tags=["years"], response_model=list[Year])
async def get_all_emissions(
    db: Session = Depends(get_db), skip: int = 0, limit: int = 200
):
    """
    Get all emissions data

    Args:
        db (Session, optional): DB session. Defaults to Depends(get_db).
        skip (int, optional): How many results to skip. Defaults to 0.
        limit (int, optional): Limit on how many results to return. Defaults to 200.

    Returns:
        _type_: _description_
    """
    emissions = crud.get_all_emissions(db, skip=skip, limit=limit)
    return emissions


@router.get("/year/{year}", tags=["years"], response_model=list[Year])
async def get_yearly_emissions(year: int, db: Session = Depends(get_db)):
    """Get year objects for a given year

    Args:
        year (int): The year to get emissions for
        db (Session, optional): DB session. Defaults to Depends(get_db).

    Raises:
        HTTPException: 404 if year not found

    Returns:
        list[Year]: List of Year objects
    """
    emissions = crud.get_emissions(db, year)
    if emissions is None:
        raise HTTPException(status_code=404, detail="Year not found")
    return emissions


@router.get("/year/{year}/total", tags=["years"], response_model=float)
async def get_total_emissions(year: int, db: Session = Depends(get_db)):
    """
    Get the total emissions for a given year

    Args:
        year (int): The year to get emissions for
        db (Session, optional): DB session. Defaults to Depends(get_db).

    Raises:
        HTTPException: 404 if year not found

    Returns:
        float: total emissions
    """
    emissions = crud.get_emissions(db, year)
    if emissions is None:
        raise HTTPException(status_code=404, detail="Year not found")
    total_emissions = 0.0
    for em in emissions:
        if em.scope1_2_3 is not None:
            total_emissions += em.scope1_2_3
        elif em.scope1_2 is not None:
            total_emissions += em.scope1_2
    return total_emissions


@router.get("/year/{year}/scope_1_2", tags=["years"], response_model=float)
async def get_scope1_2_emissions(year: int, db: Session = Depends(get_db)):
    """
    Get the scope 1 and 2 emissions for a given year

    Args:
        year (int): The year to get emissions for
        db (Session, optional): DB session. Defaults to Depends(get_db).

    Raises:
        HTTPException: 404 if year not found

    Returns:
        float: scope 1+2 emissions
    """
    emissions = crud.get_emissions(db, year)
    if emissions is None:
        raise HTTPException(status_code=404, detail="Year not found")
    total_emissions = 0.0
    for em in emissions:
        if em.scope1_2 is not None:
            total_emissions += em.scope1_2
    return total_emissions


@router.get("/year/{year}/scope_3", tags=["years"], response_model=float)
async def get_scope3_emissions(year: int, db: Session = Depends(get_db)):
    """
    Get the scope 3 emissions for a given year

    Args:
        year (int): The year to get emissions for
        db (Session, optional): DB session. Defaults to Depends(get_db).

    Raises:
        HTTPException: 404 if year not found

    Returns:
        float: scope 3 emissions
    """
    # Get total emissions and subtract scope 1 and 2 emissions
    scope3 = crud.get_scope3_emissions(db, year)
    if scope3 is None:
        raise HTTPException(status_code=404, detail="Year not found")
    return scope3
