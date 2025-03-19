from pydantic import BaseModel, ConfigDict, Field
from fastapi_filter.contrib.sqlalchemy import Filter
from models.oap import OapProgramDB
from datetime import datetime


class OapProgramFilter(Filter):
    order_by: list[str] | None = None
    name: str | None = None
    name__in: list[str] | None = None

    class Constants(Filter.Constants):
        model = OapProgramDB


class OapProgramCreate(BaseModel):
    name: str
    import_path: str
    create_date: datetime | None = None
    oap_version: str
    description: str | None = None

    model_config = ConfigDict(from_attributes=True)


class OapProgramUpdate(OapProgramCreate):
    id: int
    deleted: bool


class OapProgramOut(OapProgramUpdate):
    pass
 