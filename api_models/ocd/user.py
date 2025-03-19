from typing import Any
from pydantic import BaseModel, ConfigDict, Field
from fastapi_filter.contrib.sqlalchemy import Filter
from models.ocd import OcdUserDB, UserRole


class OcdUserFilter(Filter):
    order_by: list[str] | None = None
    email: str | None = None
    email__in: list[str] | None = None

    class Constants(Filter.Constants):
        model = OcdUserDB


class OcdUserCreate(BaseModel):
    email: str
    password: str


class OcdUserUpdate(OcdUserCreate):
    id: int


class OcdUserOut(BaseModel):
    id: int
    email: str
    hashed_password: str
    role: UserRole = UserRole.USER
    model_config = ConfigDict(from_attributes=True)
