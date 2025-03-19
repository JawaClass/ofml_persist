from pydantic import BaseModel, ConfigDict, Field
from fastapi_filter.contrib.sqlalchemy import Filter
from api_models.oap import OapBaseFilter
from models.oap import OapObjectDB, ObjectCategory


class OapObjectFilter(OapBaseFilter):

    class Constants(Filter.Constants):
        model = OapObjectDB


class OapObjectCreate(BaseModel):
    program_id: int
    name: str
    category: ObjectCategory
    argument1: str | None = None
    argument2: str | None = None
    argument3: str | None = None

    model_config = ConfigDict(from_attributes=True)


class OapObjectUpdate(OapObjectCreate):
    id: int


class OapObjectOut(OapObjectUpdate):
    pass
