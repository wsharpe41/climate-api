"""Goal model"""
from pydantic import BaseModel


class Goal(BaseModel):
    """Goal model for the API"""
    id: int
    scope12_target_year: int = None
    scope12_percent_decrease: float = None
    scope3_target_year: int = None
    scope3_percent_decrease: float = None
    reference_year: int = None

    class Config:
        """Pydantic ORM mode"""
        orm_mode = True
