from pydantic import BaseModel, ConfigDict
from fastapi_filter.contrib.sqlalchemy import Filter
from .text import OcdTextOut
from models.ocd import OcdPropertyValueDB


class OcdPropertyvalueFilter(Filter):
    order_by: list[str] | None = None
    property_class_id: int | None = None
    property_id: int | None = None
    value_from: str | None = None

    class Constants(Filter.Constants):
        model = OcdPropertyValueDB


class OcdPropertyvalueCreate(BaseModel):
    property_id: int
    text_id: int | None = None
    relobj_id: int | None = None
    pos_pval: int
    is_default: int
    suppress_txt: int
    op_from: str | None = None
    value_from: str | None = None
    op_to: str | None = None
    value_to: str | None = None
    raster: str | None = None
    disabled: bool | None = None


class OcdPropertyvalueUpdate(OcdPropertyvalueCreate):
    id: int


class OcdPropertyvalueOut(OcdPropertyvalueCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)


class OcdPropertyvalueWithTextOut(OcdPropertyvalueOut):
    ref_text: OcdTextOut | None = None
