"""Year model"""
from typing import Optional
from pydantic import BaseModel


class Year(BaseModel):
    """Year model for the API"""

    id: int
    year: int
    scope1_2: Optional[float] = None
    scope1_2_3: Optional[float] = None

    class Config:
        """Pydantic ORM mode"""

        orm_mode = True
