# Read in a csv file from a given path and return each page as a pandas dataframe
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Import from climate-api
# do the sys.path.append thing
import sys
from climate_api.internal.Year import Year
from climate_api.internal.Goal import Goal
from climate_api.internal.Company import Company
import os

# import os.path
sys.path.append("S:\PycharmProjects\climate-api\src\climate_api")


def read_csv(path: str) -> pd.DataFrame:
    # Get all sheets from the excel file
    xls = pd.ExcelFile(path)
    emissions_data = pd.read_excel(xls, "All_Emissions_Data")
    goals = pd.read_excel(xls, "Goals")
    scope12 = pd.read_excel(xls, "Scope_1_2_Data")
    scope123 = pd.read_excel(xls, "Scope_1_2_3_Data")
    return emissions_data, goals, scope12, scope123


# Create a connection to the database
def connect_to_db() -> None:
    # Create an engine to connect to the database
    # Get user variable pg_pass from environment
    pg_pass = os.environ.get("pg_pass")
    engine = create_engine(f"postgresql+psycopg2://postgres:{pg_pass}@localhost:5432/climate_api")
    # Create a session to interact with the database
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


# For each row in goals, create a row in the goals table in the database
def populate_goals(goals: pd.DataFrame, session) -> None:
    """_summary_

    Args:
        goals (pd.DataFrame): _description_
        session (_type_): _description_
    """
    goal_id = 1
    for _, row in goals.iterrows():
        goal = Goal(
            id=goal_id,
            scope12_target_year=row["Scope 1,2 Year"],
            scope12_percent_decrease=row["Scope 1,2 Goal"],
            scope3_target_year=row["Scope 1,2,3 Year"],
            scope3_percent_decrease=row["Scope 1,2,3 Goal"],
            reference_year=row["Reference Year"],
        )
        print(row)
        # Get the Company Name and Link columns from the goals dataframe
        company_name = row["Company Name"]
        report_link = row["Link"]
        #  For every column in goal make and nans into a None
        for column in goal.__dict__: 
            if goal.__dict__[column] != goal.__dict__[column]:
                goal.__dict__[column] = None
        
        
        session.add(goal)
        company = session.query(Company).filter(Company.title == company_name).first()
        print(company,company_name)
        company.goals = goal_id
        company.report_link = report_link
        goal_id += 1

    session.commit()


# For each row in the emissions_data make a Year object and add it to the emissions dictionary
def populate_emissions(
    emissions_data: pd.DataFrame, scope12: pd.DataFrame, scope123: pd.DataFrame, session
) -> None:
    """_summary_

    Args:
        emissions_data (pd.DataFrame): _description_
        session (_type_): _description_
    """
    # Each row in the scope12 dataframe is a company
    # Each row in the scope123 dataframe is a company
    # The Company Name Column is Name+ 1+2 in scope12 and Name+ 1+2+3 in scope123
    # Each column after the company name is a year from 2005 to 2023

    # Merge scope12 and scope123 on the company name minus the 1+2 or 1+2+3
    # This will give us a dataframe with the company name and all the years from 2005 to 2023
    # In scope12 and scope123 strip the company name of the 1+2 or 1+2+3 and merge the two dataframes on the company name
    scope12["Company Name"] = scope12["Company Name"].str.replace("1+2", "")
    scope123["Company Name"] = scope123["Company Name"].str.replace("1+2+3", "")
    # Now that the company names are the same we can merge the two dataframes
    # We will use an outer join so that we keep all the rows from both dataframes
    merged_scope = scope12.merge(scope123, on="Company Name", how="outer")
    company_id = 1
    id_num = 1
    for _, row in merged_scope.iterrows():
        # Create a dictionary to hold the years and their emissions
        emissions = {}
        # For each year in the row, create a Year object and add it to the emissions dictionary
        for year in range(2005, 2024):
            id_num += 1
            if year == 2007:
                continue
            emissions[year] = Year(
                id=id_num,
                year=year,
                scope1_2=row[f"{year}_x"],
                scope1_2_3=row[f"{year}_y"],
            )
            # Add each year to the years table in the database
            session.add(emissions[year])
        # Create a company object and add it to the database

        company = Company(
            id=company_id,
            title=row["Company Name"],
        )
        session.add(company)
        session.commit()

        # Add to companies_years table an entry with the company id and the year id
        for year in emissions:
            session.execute(
                "INSERT INTO company_years (company_id, year_id) VALUES (:company_id, :year_id)",
                {"company_id": company.id, "year_id": emissions[year].id},
            )

        company_id += 1
        print(company)
 
    session.commit()


if __name__ == "__main__":
    # Read in the data
    emissions_data, goals, scope12, scope123 = read_csv(
        "C:\\Users\\Will\\Downloads\\Fortune_500_fixed.xlsx"
    )
    # Connect to the database
    session = connect_to_db()
    # Populate the goals table
    #
    # Populate the emissions table
    #populate_emissions(emissions_data, scope12, scope123, session)   
    populate_goals(goals, session)
