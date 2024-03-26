from pydantic import BaseModel


class Company(BaseModel):
    id: int
    title: str
    description: str = None
    goals: int = None
    report_link: str = None
    
    class Config:
        orm_mode = True
    
        
spells = [None,None,None]

# Unlock spell
spell = [[], None, None]

spell = list[list[Company]]
