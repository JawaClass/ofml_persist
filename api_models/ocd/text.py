from typing import Optional
from pydantic import BaseModel, ConfigDict
from fastapi_filter.contrib.sqlalchemy import Filter

from models.ocd import OcdTextDB, TextType


class OcdTextFilter(Filter):
    order_by: list[str] | None = None
    text_type: TextType | None = None

    class Constants(Filter.Constants):
        model = OcdTextDB


class OcdTextCreate(BaseModel):
    program_id: int
    text_type: TextType
    text_de: None | str = None
    text_en: None | str = None
    text_fr: None | str = None
    text_nl: None | str = None


class OcdTextUpdate(OcdTextCreate):
    id: int


class OcdTextOut(OcdTextCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)
