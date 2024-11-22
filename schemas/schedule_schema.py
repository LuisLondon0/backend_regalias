from pydantic import BaseModel, Field

class ScheduleCreate(BaseModel):
    task_id: int = Field(..., description="ID of the task")
    month_id: int = Field(..., description="ID of the month")

class ScheduleResponse(ScheduleCreate):
    id: int = Field(..., description="Unique identifier for the schedule")