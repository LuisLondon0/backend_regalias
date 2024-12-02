from typing import Optional
from pydantic import BaseModel, Field

class ActivityCreate(BaseModel):
    specific_objective_id: int = Field(..., description="ID of the specific objective")
    description: str = Field(..., description="Description of the activity")
    product: Optional[str] = Field(None, description="Result that will be obtained by carrying out the activity (if applicable)")
    verification_method: Optional[str] = Field(None, description="The way in which compliance with the activity will be verified (if applicable)")
    product_indicator: Optional[str] = Field(None, description="Quantity of products (if applicable)")

class ActivityResponse(ActivityCreate):
    id: int = Field(..., description="Unique identifier for the activity")