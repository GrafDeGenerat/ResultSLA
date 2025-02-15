from datetime import datetime

from fastapi import HTTPException
from pydantic import BaseModel, Field, PositiveFloat, model_validator


class RequestModel(BaseModel):
    date: datetime = Field(default=datetime.now())
    operating_mode_from: int | float = Field(ge=0.0, le=24.0)
    operating_mode_to: int | float = Field(ge=0.0, le=24.0)
    sla_time: PositiveFloat

    @model_validator(mode="before")
    def check_model(cls, values):
        if not values.get("operating_mode_from") or not values.get("operating_mode_to"):
            raise HTTPException(status_code=400, detail="Operating modes cannot be empty")
        return values


class ResponseModel(BaseModel):
    deadline: datetime
