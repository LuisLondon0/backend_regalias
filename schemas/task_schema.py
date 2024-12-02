from typing import Optional
from pydantic import BaseModel, Field

class TaskCreate(BaseModel):
    activity_id: int = Field(..., description="ID of the activity")
    description: str = Field(..., description="Description of the general objective")
    responsible: Optional[str] = Field(None, description="Entity responsible for the activity (if applicable)")
    required_personnel: Optional[str] = Field(None, description="Description of the ideal professional to carry out the task")
    activity_results: Optional[str] = Field(None, description="Result that will be obtained by carrying out the task (if applicable)")
    technical_requirement: Optional[str] = Field(None, description="Technical, technological, and logistical requirements to complete the task (if applicable)")

class TaskResponse(TaskCreate):
    id: int = Field(..., description="Unique identifier for the task")