"""Goal model"""
from typing import Optional
from pydantic import BaseModel


class Goal(BaseModel):
    """Goal model for the API"""

    id: int
    scope12_target_year: Optional[int] = None
    scope12_percent_decrease: Optional[float] = None
    scope3_target_year: Optional[int] = None
    scope3_percent_decrease: Optional[float] = None
    reference_year: Optional[int] = None

    class Config:
        """Pydantic ORM mode"""

        orm_mode = True
