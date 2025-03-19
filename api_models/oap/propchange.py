from pydantic import BaseModel, ConfigDict, Field
from fastapi_filter.contrib.sqlalchemy import Filter
from api_models.oap import OapBaseFilter
from models.oap import OapPropChangeDB, PropChangeType


class OapPropChangeFilter(OapBaseFilter):

    class Constants(Filter.Constants):
        model = OapPropChangeDB


class OapPropChangeCreate(BaseModel):
    program_id: int
    name: str
    type: PropChangeType
    property: str
    value: str

    model_config = ConfigDict(from_attributes=True)


class OapPropChangeUpdate(OapPropChangeCreate):
    id: int


class OapPropChangeOut(OapPropChangeUpdate):
    pass
