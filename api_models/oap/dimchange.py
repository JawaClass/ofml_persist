from pydantic import BaseModel, ConfigDict, Field
from fastapi_filter.contrib.sqlalchemy import Filter
from api_models.oap import OapBaseFilter
from models.oap import DimChangeDimension, OapPropEditDB, StateRestrType


class OapDimChangeFilter(OapBaseFilter):

    class Constants(Filter.Constants):
        model = OapPropEditDB


class OapDimChangeCreate(BaseModel):
    program_id: int
    name: str
    dimension: DimChangeDimension
    condition: str | None = None
    separate: str | None = None
    third_dim: str | None = None
    property: str | None = None
    multiplier: str | None = None
    precision: str | None = None

    model_config = ConfigDict(from_attributes=True)


class OapDimChangeUpdate(OapDimChangeCreate):
    id: int


class OapDimChangeOut(OapDimChangeUpdate):
    pass
