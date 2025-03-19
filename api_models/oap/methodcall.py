from pydantic import BaseModel, ConfigDict, Field
from fastapi_filter.contrib.sqlalchemy import Filter
from api_models.oap import OapBaseFilter
from models.oap import MethodCallType, OapMethodCallDB


class OapMethodCallFilter(OapBaseFilter):

    class Constants(Filter.Constants):
        model = OapMethodCallDB


class OapMethodCallCreate(BaseModel):
    program_id: int
    name: str
    type: MethodCallType
    context: str
    method: str
    arguments: str | None = None

    model_config = ConfigDict(from_attributes=True)


class OapMethodCallUpdate(OapMethodCallCreate):
    id: int


class OapMethodCallOut(OapMethodCallUpdate):
    pass
