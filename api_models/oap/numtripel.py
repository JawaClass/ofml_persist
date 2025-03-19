from pydantic import BaseModel, ConfigDict, Field
from fastapi_filter.contrib.sqlalchemy import Filter
from api_models.oap import OapBaseFilter
from models.oap import OapNumTripelDB


class OapNumTripelFilter(OapBaseFilter):

    class Constants(Filter.Constants):
        model = OapNumTripelDB


class OapNumTripelCreate(BaseModel):
    program_id: int
    name: str
    x: str
    y: str
    z: str

    model_config = ConfigDict(from_attributes=True)


class OapNumTripelUpdate(OapNumTripelCreate):
    id: int


class OapNumTripelOut(OapNumTripelUpdate):
    pass


class OapNumTripelItemOut(OapNumTripelOut):
    pass
