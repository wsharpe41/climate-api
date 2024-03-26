from pydantic import BaseModel


class Year(BaseModel):
    id: int
    year: int
    scope1_2: float = None
    scope1_2_3: float = None
    
    class Config:
        orm_mode = True