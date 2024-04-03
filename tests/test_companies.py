"""Test the companies endpoint."""

from fastapi.testclient import TestClient
from src.climate_api.routers.companies import router
from src.climate_api.models import Company, Year, Goal
from pydantic import ValidationError

client = TestClient(router)


def test_get_companies_list():
    """Test the /companies endpoint."""
    response = client.get("/companies")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_company():
    """Test the /companies/{company} endpoint."""
    response = client.get("/companies/Apple")
    assert response.status_code == 200
    assert response.json()["title"] == "Apple"
    try:
        Company(**response.json())
    except ValidationError as e:
        assert False, f"Response data does not match Company model: {e}"


def test_get_all_company_data():
    """Test the /companies/{company}/all_years endpoint."""
    response = client.get("/companies/Apple/all_years")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    year_data = response.json()[0]
    try:
        Year(**year_data)
    except ValidationError as e:
        assert False, f"Response data does not match Year model: {e}"


def test_get_company_change_1_2():
    """Test the /companies/{company}/change_1_2 endpoint."""
    response = client.get("/companies/Apple/change_1_2")
    assert response.status_code == 200
    assert isinstance(response.json(), float)
    response = client.get("/companies/Apple/change_1_2?percent=True")
    assert response.status_code == 200


def test_get_company_change_1_2_3():
    """Test the /companies/{company}/change_1_2_3 endpoint."""
    response = client.get("/companies/Apple/change_1_2_3")
    assert response.status_code == 200
    assert isinstance(response.json(), float)
    response = client.get("/companies/Apple/change_1_2_3?percent=True")
    assert response.status_code == 200


def test_get_company_change_with_year_1_2():
    """Test the /companies/{company}/change_1_2/{start_year}_{end_year} endpoint."""
    response = client.get("/companies/Apple/change_1_2/2019_2022")
    assert response.status_code == 200
    assert isinstance(response.json(), float)


def test_get_company_change_with_year_1_2_3():
    """Test the /companies/{company}/change_1_2_3/{start_year}_{end_year} endpoint."""
    response = client.get("/companies/Apple/change_1_2_3/2019_2022")
    assert response.status_code == 200
    assert isinstance(response.json(), float)


def test_get_company_goal():
    """Test the /companies/{company}/goals endpoint."""
    response = client.get("/companies/Apple/goals")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    try:
        Goal(**response.json())
    except ValidationError as e:
        assert False, f"Response data does not match Goal model: {e}"


def test_get_company_year():
    """Test the /companies/{company}/{year} endpoint."""
    response = client.get("/companies/Apple/2019")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    try:
        Year(**response.json())
    except ValidationError as e:
        assert False, f"Response data does not match Year model: {e}"
