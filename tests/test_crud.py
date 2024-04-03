"""Test the CRUD operations."""
import math
import unittest
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.climate_api.crud import (
    get_companies,
    get_company,
    get_company_year,
    get_company_years,
    get_goal,
    get_emissions,
    get_all_emissions,
    get_scope3_emissions,
)


class TestCrudMethods(unittest.TestCase):
    """Class to test the CRUD operations."""

    @classmethod
    def setUpClass(cls):
        database_url = os.environ.get("HEROKU_DATABASE_URL")
        database_url = database_url.replace("postgres://", "postgresql://", 1)
        engine = create_engine(
            database_url,
        )
        Session = sessionmaker(bind=engine)
        cls.session = Session()

    @classmethod
    def tearDownClass(cls):
        cls.session.close()

    def test_get_companies(self):
        """Test getting a list of companies."""
        companies = get_companies(self.session, limit=10)
        self.assertEqual(len(companies), 10)

    def test_get_company(self):
        """Test getting a single company."""
        company = get_company(self.session, "Walmart")
        self.assertIsNotNone(company)
        self.assertEqual(company.title, "Walmart")

    def test_get_company_year(self):
        """Test getting a single company year."""
        company_year = get_company_year(self.session, "Walmart", 2022)
        self.assertIsNotNone(company_year)
        self.assertEqual(company_year.year, 2022)

    def test_get_company_years(self):
        """Test getting a list of company years."""
        company_years = get_company_years(self.session, "Walmart")
        self.assertIsNotNone(company_years)
        self.assertEqual(len(company_years), 18)

    def test_get_goal(self):
        """Test getting a goal."""
        goal = get_goal(self.session, 1)
        self.assertIsNotNone(goal)
        self.assertEqual(goal.id, 1)

    def test_get_emissions(self):
        """Test getting a list of emissions."""
        emissions = get_emissions(self.session, 2023, limit=10)
        self.assertIsNotNone(emissions)
        self.assertEqual(len(emissions), 10)

    def test_get_all_emissions(self):
        """Test getting all emissions."""
        all_emissions = get_all_emissions(self.session, limit=10)
        self.assertIsNotNone(all_emissions)
        self.assertEqual(len(all_emissions), 10)

    def test_get_scope3_emissions(self):
        """Test getting scope 3 emissions."""
        scope3_emissions = get_scope3_emissions(self.session, 2022)
        self.assertEqual(math.floor(scope3_emissions), 3819)


if __name__ == "__main__":
    unittest.main()
