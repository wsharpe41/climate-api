"""Main module for the FastAPI application."""
from fastapi import FastAPI
from .routers import companies, years


app = FastAPI()

app.include_router(companies.router)
app.include_router(years.router)
