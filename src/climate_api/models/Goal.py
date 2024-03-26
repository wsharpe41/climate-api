from pydantic import BaseModel


class Goal(BaseModel):
    id: int
    scope12_target_year: int = None
    scope12_percent_decrease: float = None
    scope3_target_year: int = None
    scope3_percent_decrease: float = None
    reference_year: int = None
    
    class Config:
        orm_mode = True