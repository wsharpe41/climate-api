"""Company model"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Company(Base):
    """Company model for the database."""

    __tablename__ = "companies"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String, nullable=True)
    goals = Column(Integer, nullable=True)  # Assuming you'll store goals as JSON data
    report_link = Column(String, nullable=True)

    def __repr__(self):
        return f"<Company(id={self.id}, title={self.title}, description={self.description})>"
