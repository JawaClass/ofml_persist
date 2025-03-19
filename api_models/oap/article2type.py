from pydantic import BaseModel, ConfigDict, Field
from fastapi_filter.contrib.sqlalchemy import Filter
from api_models.oap import OapBaseFilter
from models.oap import OapArticle2TypeDB


class OapArticle2TypeFilter(OapBaseFilter):
    series_id: str | None = None
    article_id: str | None = None
    series_id__in: list[str] | None = None
    article_id__in: list[str] | None = None
    var_type: str | None = None
    type_id: int | None = None

    class Constants(Filter.Constants):
        model = OapArticle2TypeDB


class OapArticle2TypeCreate(BaseModel):
    program_id: int
    manufacturer_id: str
    series_id: str
    article_id: str
    var_type: str | None = None
    type_id: int

    model_config = ConfigDict(from_attributes=True)


class OapArticle2TypeUpdate(OapArticle2TypeCreate):
    id: int


class OapArticle2TypeOut(OapArticle2TypeUpdate):
    pass
