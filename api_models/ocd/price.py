from pydantic import BaseModel, ConfigDict
from models.ocd import OcdPriceDB
from .text import OcdTextCreate
from fastapi_filter.contrib.sqlalchemy import Filter

class OcdPriceFilter(Filter):
    order_by: list[str] | None = None
    article_id: int | None = None
    price_type: str | None = None
    price_level: str | None = None
    class Constants(Filter.Constants):
        model = OcdPriceDB


class OcdPriceCreateBase(BaseModel):
    article_id: int
    var_cond: str | None = None
    price_type: str
    price_level: str
    price_rule: str | None = None
    price: str | float
    is_fix: int
    currency: str
    date_from: str
    date_to: str
    scale_quantity: int
    rounding_id: int | None = None
    

class OcdPriceCreateWithText(OcdPriceCreateBase):
    text: OcdTextCreate


class OcdPriceCreateWithoutText(OcdPriceCreateBase):
    price_text_id: int | None = None


class OcdPriceUpdate(OcdPriceCreateWithoutText):
    id: int 


class OcdPriceOut(OcdPriceCreateWithoutText):
    id: int
    model_config = ConfigDict(from_attributes=True)