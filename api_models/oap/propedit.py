from pydantic import BaseModel, ConfigDict, Field
from fastapi_filter.contrib.sqlalchemy import Filter
from api_models.oap import OapBaseFilter
from api_models.oap.text import OapTextOut
from models.oap import OapPropEditDB, StateRestrType


class OapPropEditFilter(OapBaseFilter):

    class Constants(Filter.Constants):
        model = OapPropEditDB


class OapPropEditCreate(BaseModel):
    program_id: int
    name: str
    state_restr: StateRestrType
    properties: str | None = None
    classes: str | None = None
    title_id: int | None = None

    model_config = ConfigDict(from_attributes=True)


class OapPropEditUpdate(OapPropEditCreate):
    id: int


class OapPropEditOut(OapPropEditUpdate):
    pass


class OapPropEditItemOut(OapPropEditOut):
    ref_title: OapTextOut | None = None
