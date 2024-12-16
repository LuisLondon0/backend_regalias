from pydantic import BaseModel, Field
from typing import Optional

class FeeValueCreate(BaseModel):
    managmentlevel: Optional[str] = Field(None, description="Name of the managment level")
    category: Optional[str] = Field(None, description="Name of the category")
    academicsuitability: Optional[str] = Field(None, description="Name of the academic suitability")
    minimumexperience: Optional[int] = Field(None, description="Minimum experience required")
    monthlyfee: Optional[float] = Field(None, description="Monthly fee")
    monthlyfeewithtaxes: Optional[float] = Field(None, description="Monthly fee with taxes")

class FeeValueResponse(FeeValueCreate):
    id: int = Field(..., description="Unique identifier for the fee value")