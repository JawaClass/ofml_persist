from pydantic import BaseModel, ConfigDict, Field
from fastapi_filter.contrib.sqlalchemy import Filter
from api_models.oap import OapBaseFilter
from api_models.oap.numtripel import OapNumTripelOut
from models.oap import OapSymbolDisplayDB, OffsetType


class OapSymbolDisplayFilter(OapBaseFilter):
    order_by: list[str] | None = None
    name: str | None = None
    name__in: list[str] | None = None
    id__in: list[int] | None = None

    class Constants(Filter.Constants):
        model = OapSymbolDisplayDB


class OapSymbolDisplayCreate(BaseModel):
    program_id: int
    interactor_id: int
    hidden_mode: bool | None = None
    offset_type: OffsetType
    offset_id: int | None = None
    offset_expr: str | None = None
    direction_id: int | None = None
    view_angle: str | None = None
    orientation_x_id: int | None = None

    model_config = ConfigDict(from_attributes=True)


class OapSymbolDisplayUpdate(OapSymbolDisplayCreate):
    id: int


class OapSymbolDisplayOut(OapSymbolDisplayUpdate):
    pass


class OapSymbolDisplayItemOut(OapSymbolDisplayOut):
    ref_offset: OapNumTripelOut | None = None
    ref_direction: OapNumTripelOut | None = None
    ref_orientation_x: OapNumTripelOut | None = None
