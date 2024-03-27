"""Year model"""

from pydantic import BaseModel


class Year(BaseModel):
    """Year model for the API"""

    id: int
    year: int
    scope1_2: float = None
    scope1_2_3: float = None

    class Config:
        """Pydantic ORM mode"""

        orm_mode = True
