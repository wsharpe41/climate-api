from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Goal(Base):
    __tablename__ = "goals"

    id = Column(Integer, primary_key=True)
    scope12_target_year = Column(Integer)
    scope12_percent_decrease = Column(Float)
    scope3_target_year = Column(Integer)
    scope3_percent_decrease = Column(Float)
    reference_year = Column(Integer)

    def __repr__(self):
        return f"<Goal(id={self.id})>"
