from pydantic import BaseModel, ConfigDict, Field
from fastapi_filter.contrib.sqlalchemy import Filter
from api_models.oap.article2type import OapArticle2TypeOut
from api_models.oap.interactor import OapInteractorOut
from api_models.oap.metatype2type import OapMetaType2TypeOut
from models.oap import OapTypeDB


class OapTypeFilter(Filter):
    order_by: list[str] | None = None
    name: str | None = None
    name__in: list[str] | None = None
    program_id: int | None = None

    class Constants(Filter.Constants):
        model = OapTypeDB


class OapTypeCreate(BaseModel):
    program_id: int
    name: str
    general_info: str | None = None
    prop_change_actions: str | None = None
    active_att_areas: str | None = None
    passive_att_areas: str | None = None

    model_config = ConfigDict(from_attributes=True)


class OapTypeUpdate(OapTypeCreate):
    id: int


class OapTypeOut(OapTypeUpdate):
    pass


class OapTypeItemOut(OapTypeUpdate):
    ref_interactor: list[OapInteractorOut]
    ref_article2type: list[OapArticle2TypeOut] = []
    ref_metatypetype: list[OapMetaType2TypeOut] = []
