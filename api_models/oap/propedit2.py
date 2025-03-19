from pydantic import BaseModel, ConfigDict, Field
from fastapi_filter.contrib.sqlalchemy import Filter
from api_models.oap import OapBaseFilter
from api_models.oap.propeditprops import OapPropEditPropsListOut
from models.oap import OapPropEdit2DB


class OapPropEdit2Filter(OapBaseFilter):

    class Constants(Filter.Constants):
        model = OapPropEdit2DB


class OapPropEdit2Create(BaseModel):
    program_id: int
    name: str
    title_id: int | None = None
    propeditprops_list_id: int | None = None
    propeditclasses_list_id: int | None = None

    model_config = ConfigDict(from_attributes=True)


class OapPropEdit2Update(OapPropEdit2Create):
    id: int


class OapPropEdit2Out(OapPropEdit2Update):
    pass


class OapPropEdit2ItemOut(OapPropEdit2Out):
    ref_propeditprops_list: OapPropEditPropsListOut
