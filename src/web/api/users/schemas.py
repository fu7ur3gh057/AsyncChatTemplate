from pydantic import BaseModel, Field
from datetime import datetime


class UserIn(BaseModel):
    external_id: str


class UserOut(BaseModel):
    id: int
    external_id: str
    created_at: datetime

    model_config = {"from_attributes": True}  # вместо orm_mode
