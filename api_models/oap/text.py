from pydantic import BaseModel, ConfigDict, Field
from fastapi_filter.contrib.sqlalchemy import Filter
from models.oap import OapTextDB


class OapTextFilter(Filter):
    order_by: list[str] | None = None
    name: str | None = None
    name__in: list[str] | None = None
    text_de: str | None = None
    text_de__like: str | None = None
    program_id: int | None = None

    class Constants(Filter.Constants):
        model = OapTextDB


class OapTextCreate(BaseModel):
    program_id: int
    name: str
    text_de: str | None = None
    text_en: str | None = None
    text_fr: str | None = None
    text_nl: str | None = None

    model_config = ConfigDict(from_attributes=True)


class OapTextUpdate(OapTextCreate):
    id: int


class OapTextOut(OapTextUpdate):
    pass
