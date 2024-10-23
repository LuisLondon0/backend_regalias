from pydantic import BaseModel

class WeekCreate(BaseModel):
    week: int

class WeekResponse(WeekCreate):
    id: int