from pydantic import BaseModel, ConfigDict, Field
from fastapi_filter.contrib.sqlalchemy import Filter
from api_models.oap import OapBaseFilter
from api_models.oap.object import OapObjectOut
from models.oap import ArtSpecMode, OapCreateObjDB, PosRotMode


class OapCreateObjFilter(OapBaseFilter):

    class Constants(Filter.Constants):
        model = OapCreateObjDB


class OapCreateObjCreate(BaseModel):
    program_id: int
    name: str
    parent_id: int | None = None  # have to allow None here for GUI handling
    art_spec_mode: ArtSpecMode
    package: str
    article_id: str
    var_code: str | None = None
    pos_rot_mode: PosRotMode
    pos_rot_arg1: str
    pos_rot_arg2: str
    pos_rot_arg3: str | None = None

    model_config = ConfigDict(from_attributes=True)


class OapCreateObjUpdate(OapCreateObjCreate):
    id: int


class OapCreateObjOut(OapCreateObjUpdate):
    pass


class OapCreateObjOutItem(OapCreateObjOut):
    ref_parent: OapObjectOut | None = None
