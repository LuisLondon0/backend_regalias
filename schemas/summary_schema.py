from pydantic import BaseModel, Field
from decimal import Decimal
from typing import Optional
from typing import List

class Summary(BaseModel):
    heading: str = Field(..., description="Budget heading")
    totalsgr: Decimal = Field(..., description="Total SGR of the project", ge=0)

# Modelo para la respuesta que incluye una lista de summaries
class SummaryResponse(BaseModel):
    response: List[Summary] = Field(..., description="List of budget summaries")

# class SummaryResponse(Summary):
#     id: int = Field(..., description="Unique identifier for the project")