"""Year model."""
from sqlalchemy import Column, Integer, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Year(Base):
    """Year model for the database."""

    __tablename__ = "years"

    id = Column(Integer, primary_key=True)
    year = Column(Integer, nullable=False)
    scope1_2 = Column(Float, nullable=True)
    scope1_2_3 = Column(Float, nullable=True)

    def __repr__(self):
        return f"<Year(id={self.id}, year={self.year})>"
