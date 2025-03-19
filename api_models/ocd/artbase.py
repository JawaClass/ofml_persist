from typing import Optional
from pydantic import BaseModel, ConfigDict
from fastapi_filter.contrib.sqlalchemy import Filter

from models.ocd import OcdArtbaseDB


class OcdArtbaseFilter(Filter):
    order_by: list[str] | None = None
    article_id: Optional[int] = None
    class_name: Optional[str] = None
    prop_name: Optional[str] = None
    prop_value: Optional[str] = None

    class Constants(Filter.Constants):
        model = OcdArtbaseDB


class OcdArtbaseCreate(BaseModel):
    article_id: int
    class_name: str
    prop_name: str
    prop_value: str | int


class OcdArtbaseOut(OcdArtbaseCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)
