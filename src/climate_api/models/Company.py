"""Company pydantic model"""
from pydantic import BaseModel


class Company(BaseModel):
    """Company model for the API"""
    id: int
    title: str
    description: str = None
    goals: int = None
    report_link: str = None

    class Config:
        """Pydantic ORM mode"""
        orm_mode = True
