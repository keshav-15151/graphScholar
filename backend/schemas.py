from pydantic import BaseModel, ConfigDict, Field


class PaperCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    year: int = Field(ge=1, le=2100)


class PaperResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    year: int
    
class PaperUpdate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    year: int = Field(ge=1, le=2100)