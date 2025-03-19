from pydantic import BaseModel, ConfigDict
from fastapi_filter.contrib.sqlalchemy import Filter
from .propertyvalue import OcdPropertyvalueOut, OcdPropertyvalueWithTextOut
from .text import OcdTextOut
from models.ocd import OcdPropertyDB


class OcdPropertyFilter(Filter):
    order_by: list[str] | None = None
    property_class_id: int | None = None
    property: str | None = None
    restrictable: int | None = None
    need_input: int | None = None
    scope: str | None = None
    prop_type: str | None = None
    property__in: list[str] | None = None

    class Constants(Filter.Constants):
        model = OcdPropertyDB


class OcdPropertyCreate(BaseModel):
    property_class_id: int
    text_id: int | None = None
    text_hint_id: int | None = None
    relobj_id: int | None = None
    property: str
    pos_prop: int
    prop_type: str
    digits: int
    dec_digits: int
    need_input: int
    add_values: int
    restrictable: int
    multi_option: int
    scope: str
    txt_control: str


class OcdPropertyUpdate(OcdPropertyCreate):
    id: int


class OcdPropertyOut(OcdPropertyCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)


class OcdPropertyWithTextOut(OcdPropertyOut):
    ref_text: OcdTextOut | None = None
    ref_text_hint: OcdTextOut | None = None


class OcdPropertyItemOut(OcdPropertyWithTextOut):
    ref_property_value: list[OcdPropertyvalueWithTextOut] | None = None


class OcdPropertyItemFilter(OcdPropertyFilter):
    pass
