from pydantic import BaseModel, ConfigDict, Field
from fastapi_filter.contrib.sqlalchemy import Filter
from api_models.oap import OapBaseFilter
from models.oap import MessageArgType, OapMessageDB


class OapMessageFilter(OapBaseFilter):

    class Constants(Filter.Constants):
        model = OapMessageDB


class OapMessageCreate(BaseModel):
    program_id: int
    name: str
    arg_type: MessageArgType
    text_id: int | None = None
    action_id: int | None = None

    model_config = ConfigDict(from_attributes=True)


class OapMessageUpdate(OapMessageCreate):
    id: int


class OapMessageOut(OapMessageUpdate):
    pass
