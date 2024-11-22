from pydantic import BaseModel, Field
from decimal import Decimal
from typing import Optional

class ProjectCreate(BaseModel):
    description: str = Field(..., min_length=1, max_length=500, description="Description of the project")
    generalobjective: Optional[str] = Field(None, max_length=500, description="General objective of the project")
    projectdocument: Optional[str] = Field(None, max_length=500, description="Document related to the project")
    totalsgr: Optional[Decimal] = Field(None, description="Total SGR of the project", ge=0)
    totalduration: Optional[int] = Field(None, description="Total duration of the project in days", ge=0)

class ProjectResponse(ProjectCreate):
    id: int = Field(..., description="Unique identifier for the project")