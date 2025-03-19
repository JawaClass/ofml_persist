from pydantic import BaseModel, ConfigDict, Field
from fastapi_filter.contrib.sqlalchemy import Filter

# from api_models.oap.type import OapTypeItemOut
from api_models.oap import OapBaseFilter
from models.oap import OapMetaType2TypeDB


class OapMetaType2TypeFilter(OapBaseFilter):
    order_by: list[str] | None = None
    series_id: str | None = None
    metatype_id: str | None = None
    metatype_id__in: list[str] | None = None
    var_type: str | None = None
    type_id: int | None = None

    class Constants(Filter.Constants):
        model = OapMetaType2TypeDB


class OapMetaType2TypeCreate(BaseModel):
    program_id: int
    manufacturer: str
    series: str
    metatype_id: str
    var_type: str | None = None
    type_id: int

    model_config = ConfigDict(from_attributes=True)


class OapMetaType2TypeUpdate(OapMetaType2TypeCreate):
    id: int


class OapMetaType2TypeOut(OapMetaType2TypeUpdate):
    pass


class OapMetaType2TypeItemOut(OapMetaType2TypeOut):
    # ref_type: OapTypeItemOut
    pass
