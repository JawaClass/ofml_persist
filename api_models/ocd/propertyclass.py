from pydantic import BaseModel, ConfigDict
from fastapi_filter.contrib.sqlalchemy import Filter
from .property import OcdPropertyItemOut, OcdPropertyOut
from .text import OcdTextOut
from models.ocd import OcdPropertyClassDB


class OcdPropertyclassFilter(Filter):
    order_by: list[str] | None = None
    prop_class: str | None = None
    id__in: list[int] | None = None

    class Constants(Filter.Constants):
        model = OcdPropertyClassDB


class OcdPropertyclassCreate(BaseModel):
    text_id: int | None = None
    relobj_id: int | None = None
    pos_class: int
    prop_class: str


class OcdPropertyclassUpdate(OcdPropertyclassCreate):
    id: int


class OcdPropertyclassOut(OcdPropertyclassCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)


class OcdPropertyclassWithTextOut(OcdPropertyclassOut):
    ref_text: OcdTextOut | None = None


class OcdPropertyclassItemOut(OcdPropertyclassWithTextOut):
    ref_properties: list[OcdPropertyItemOut]
