from typing import Optional
from pydantic import BaseModel, Field

class TaskCreate(BaseModel):
    activity_id: int
    description: str = Field(..., min_length=1, max_length=500, description="Description of the general objective")
    responsible: Optional[str] = Field(None, min_length=0, max_length=255, description="Entity responsible for the activity (if applicable)")
    required_personnel: str = Field(..., min_length=1, max_length=255, description="Description of the ideal professional to carry out the task")
    activity_results: Optional[str] = Field(None, min_length=0, max_length=255, description="Result that will be obtained by carrying out the task (if applicable)")
    technical_requirement: Optional[str] = Field(None, min_length=0, max_length=255, description="Technical, technological, and logistical requirements to complete the task (if applicable)")

class TaskResponse(TaskCreate):
    id: int