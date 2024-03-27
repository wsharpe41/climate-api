"""Test the /year endpoint."""

from fastapi.testclient import TestClient
from climate_api.routers.years import router
from climate_api.models import Year
from pydantic import ValidationError

client = TestClient(router)


def test_get_all_emissions():
    """Test the /year endpoint."""
    response = client.get("/year")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    year = response.json()[0]
    try:
        Year(**year)
    except ValidationError as e:
        assert False, f"Response data does not match Year model: {e}"


def test_get_yearly_emissions():
    """Test the /year/{year} endpoint."""
    response = client.get("/year/2019")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    year = response.json()[0]
    try:
        Year(**year)
    except ValidationError as e:
        assert False, f"Response data does not match Year model: {e}"


def test_get_total_emissions():
    """Test the /year/{year}/total endpoint."""
    response = client.get("/year/2019/total")
    assert response.status_code == 200
    assert isinstance(response.json(), float)


def test_get_scope1_2_emissions():
    """Test the /year/{year}/scope_1_2 endpoint."""
    response = client.get("/year/2019/scope_1_2")
    assert response.status_code == 200
    assert isinstance(response.json(), float)
    total = client.get("/year/2019/total")
    assert total.status_code == 200
    assert response.json() <= total.json()


def test_get_scope3_emissions():
    """Test the /year/{year}/scope_3 endpoint."""
    response = client.get("/year/2019/scope_3")
    assert response.status_code == 200
    assert isinstance(response.json(), float)
    total = client.get("/year/2019/total")
    assert total.status_code == 200
    assert response.json() <= total.json()
