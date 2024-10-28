from pydantic import BaseModel

class ScheduleCreate(BaseModel):
    task_id: int
    week_id: int


class ScheduleTaskResponse(ScheduleCreate):
    id: int