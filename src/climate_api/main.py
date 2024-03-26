from fastapi import FastAPI
from .routers import companies, years
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine("sqlite:///S:\PycharmProjects\climate-api\climate-api.db")


# Dependency
# Create a connection to the database
def connect_to_db() -> None:
    # Create an engine to connect to the database
    engine = create_engine("sqlite:///S:\PycharmProjects\climate-api\climate-api.db")
    # Create a session to interact with the database
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


app = FastAPI()

app.include_router(companies.router)
app.include_router(years.router)
