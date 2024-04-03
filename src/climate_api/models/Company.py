"""Company pydantic model"""
from typing import Optional
from pydantic import BaseModel


class Company(BaseModel):
    """Company model for the API"""

    id: int
    title: str
    description: Optional[str] = None
    goals: Optional[int] = None
    report_link: Optional[str] = None

    class Config:
        """Pydantic ORM mode"""

        orm_mode = True
