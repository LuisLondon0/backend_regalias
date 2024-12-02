from pydantic import BaseModel, Field

class MonthCreate(BaseModel):
    month: str = Field(..., description="Name of the month")

class MonthResponse(MonthCreate):
    id: int = Field(..., description="Unique identifier for the month")