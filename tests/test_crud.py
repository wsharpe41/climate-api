import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from climate_api.crud import (
    get_companies,
    get_company,
    get_company_year,
    get_company_years,
    get_goal,
    get_emissions,
    get_all_emissions,
    get_scope3_emissions,
)

import math

class TestYourMethods(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        engine = create_engine('sqlite:///S:\PycharmProjects\climate-api\climate-api.db', connect_args={'check_same_thread': False})
        Session = sessionmaker(bind=engine)
        cls.session = Session()


    @classmethod
    def tearDownClass(cls):
        cls.session.close()

    def test_get_companies(self):
        companies = get_companies(self.session,limit=10)
        self.assertEqual(len(companies), 10)

    def test_get_company(self):
        company = get_company(self.session, 'Walmart')
        self.assertIsNotNone(company)
        self.assertEqual(company.title, 'Walmart')

    def test_get_company_year(self):
        company_year = get_company_year(self.session, 'Walmart', 2022)
        self.assertIsNotNone(company_year)
        self.assertEqual(company_year.year, 2022)

    def test_get_company_years(self):
        company_years = get_company_years(self.session, 'Walmart')
        self.assertIsNotNone(company_years)
        self.assertEqual(len(company_years), 18)

    def test_get_goal(self):
        # Assuming you have some Goal objects in your test data
        goal = get_goal(self.session, 1)
        self.assertIsNotNone(goal)
        self.assertEqual(goal.id, 1)

    def test_get_emissions(self):
        emissions = get_emissions(self.session, 2023,limit=10)
        self.assertIsNotNone(emissions)
        self.assertEqual(len(emissions), 10)

    def test_get_all_emissions(self):
        all_emissions = get_all_emissions(self.session,limit=10)
        self.assertIsNotNone(all_emissions)
        self.assertEqual(len(all_emissions), 1)

    def test_get_scope3_emissions(self):
        scope3_emissions = get_scope3_emissions(self.session, 2022)
        self.assertEqual(math.floor(scope3_emissions), 3688) 

if __name__ == '__main__':
    unittest.main()
