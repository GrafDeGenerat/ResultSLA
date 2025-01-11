from fastapi import HTTPException
from pydantic import BaseModel, model_validator, Field
from pydantic import PositiveFloat
from datetime import datetime


class RequestModel(BaseModel):
    date: datetime = Field(default=datetime.now())
    operating_mode_from: float = Field(ge=0, lt=24)
    operating_mode_to: float = Field(ge=0, lt=24)
    sla_time: PositiveFloat

    @model_validator(mode='before')
    def check_model(cls, values):
        if not values.get('operating_mode_from') or not values.get('operating_mode_to'):
            raise HTTPException(status_code=400, detail="Operating modes cannot be empty")
        if values.get('operating_mode_from') >= values.get('operating_mode_to'):
            raise HTTPException(status_code=400, detail="'To' value must be greater than 'From' value")
        return values


class ResponseModel(BaseModel):
    deadline: datetime


class UserModel(BaseModel):
    username: str
    password: str
