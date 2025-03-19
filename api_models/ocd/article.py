from pydantic import BaseModel, ConfigDict, Field
from fastapi_filter.contrib.sqlalchemy import Filter

from .price import OcdPriceOut
from .program import OcdProgramOut
from .propertyclass import OcdPropertyclassOut
from .text import OcdTextOut
from models.ocd import OcdArticleDB


class OcdArticleFilter(Filter):
    order_by: list[str] | None = None
    program_id: int | None = None
    article_nr: str | None = None
    article_nr__in: list[str] | None = None

    class Constants(Filter.Constants):
        model = OcdArticleDB


class OcdArticleCreate(BaseModel):
    short_text_id: int | None = None
    long_text_id: int | None = None
    relobj_id: int | None = None
    program_id: int
    article_nr: str
    art_type: str
    manufacturer: str
    series: str
    fast_supply: int = Field(default=0)
    discountable: int = Field(default=1)
    order_unit: str = Field(default="C62")
    scheme_id: str | None = None
    model_config = ConfigDict(from_attributes=True)


class OcdArticleUpdate(OcdArticleCreate):
    id: int


class OcdArticleOut(OcdArticleUpdate):
    pass


class OcdArticleWithTextOut(OcdArticleOut):
    ref_short_text: OcdTextOut
    ref_long_text: OcdTextOut


class OcdArticleWithPriceOut(OcdArticleOut):
    ref_price: list[OcdPriceOut]


class OcdArticleItemFilter(OcdArticleFilter):
    pass


class OcdUtilArticleClonedSourceOut(BaseModel):
    id: int
    src_article_nr: str
    src_series: str


class OcdArticleItemOut(OcdArticleOut):
    ref_program: OcdProgramOut
    ref_short_text: OcdTextOut
    ref_long_text: OcdTextOut | None = None
    ref_propertyclasses: list[OcdPropertyclassOut]
    ref_price_article_only_view: list[OcdPriceOut]
    ref_cloned_src: OcdUtilArticleClonedSourceOut | None = None
