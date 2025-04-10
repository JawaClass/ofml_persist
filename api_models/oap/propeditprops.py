from pydantic import BaseModel, ConfigDict, Field
from fastapi_filter.contrib.sqlalchemy import Filter
from api_models.oap import OapBaseFilter
from models.oap import OapPropEditPropsItemDB, OapPropEditPropsListDB, StateRestrType

# Item


class OapPropEditPropsItemFilter(OapBaseFilter):
    order_by: list[str] | None = None

    class Constants(Filter.Constants):
        model = OapPropEditPropsItemDB


class OapPropEditPropsItemCreate(BaseModel):
    program_id: int
    property: str | None = None  # test
    condition: str | None = None
    state_restr: StateRestrType | None = None
    list_id: int | None = None  # test ! this shouldnt be None !!!

    model_config = ConfigDict(from_attributes=True)


class OapPropEditPropsItemUpdate(OapPropEditPropsItemCreate):
    id: int


class OapPropEditPropsItemOut(OapPropEditPropsItemUpdate):
    pass


# List


class OapPropEditPropsListFilter(OapBaseFilter):
    order_by: list[str] | None = None
    name: str | None = None
    name__in: list[str] | None = None

    class Constants(Filter.Constants):
        model = OapPropEditPropsListDB


class OapPropEditPropsListCreate(BaseModel):
    name: str
    program_id: int
    model_config = ConfigDict(from_attributes=True)


class OapPropEditPropsListUpdate(OapPropEditPropsListCreate):
    id: int


class OapPropEditPropsListOut(OapPropEditPropsListUpdate):
    pass


class OapPropEditPropsListWithItemsOut(OapPropEditPropsListUpdate):
    ref_items: list[OapPropEditPropsItemOut]
