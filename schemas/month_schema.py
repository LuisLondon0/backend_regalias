from pydantic import BaseModel, Field

class MonthCreate(BaseModel):
    month: str = Field(..., min_length=1, max_length=255, description="Name of the month")

class MonthResponse(MonthCreate):
    id: int = Field(..., description="Unique identifier for the month")