from pydantic import BaseModel, ConfigDict, Field
from fastapi_filter.contrib.sqlalchemy import Filter
from api_models.oap import OapBaseFilter
from models.oap import ExtMediaType, OapExtMediaDB


class OapExtMediaFilter(OapBaseFilter):
    type: ExtMediaType | None = None
    name__in: list[str] | None = None
    id__in: list[int] | None = None
    type__in: list[ExtMediaType] | None = None

    class Constants(Filter.Constants):
        model = OapExtMediaDB


class OapExtMediaCreate(BaseModel):
    program_id: int
    name: str
    type: ExtMediaType
    media: str

    model_config = ConfigDict(from_attributes=True)


class OapExtMediaUpdate(OapExtMediaCreate):
    id: int


class OapExtMediaOut(OapExtMediaUpdate):
    pass
