"""CompanyYear model."""

from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class CompanyYear(Base):
    """CompanyYear model for the database."""

    __tablename__ = "company_years"

    company_id = Column(Integer, primary_key=True)
    year_id = Column(Integer, primary_key=True)

    def __repr__(self):
        return f"<CompanyYear(company_id={self.company_id}, year_id={self.year_id})>"
