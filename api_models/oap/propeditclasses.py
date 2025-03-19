from pydantic import BaseModel, ConfigDict, Field
from fastapi_filter.contrib.sqlalchemy import Filter
from api_models.oap import OapBaseFilter
from models.oap import (
    OapPropEditClassesItemDB,
    OapPropEditClassesListDB,
    StateRestrType,
)

# Item


class OapPropEditClassesItemFilter(OapBaseFilter):
    order_by: list[str] | None = None

    class Constants(Filter.Constants):
        model = OapPropEditClassesItemDB


class OapPropEditClassesItemCreate(BaseModel):
    prop_class: str | None = None  # test
    condition: str | None = None
    state_restr: StateRestrType | None = None
    list_id: int | None = None  # test ! this shouldnt be None !!!

    model_config = ConfigDict(from_attributes=True)


class OapPropEditClassesItemUpdate(OapPropEditClassesItemCreate):
    id: int


class OapPropEditClassesItemOut(OapPropEditClassesItemUpdate):
    pass


# List


class OapPropEditClassesListFilter(OapBaseFilter):
    order_by: list[str] | None = None
    name: str | None = None
    name__in: list[str] | None = None

    class Constants(Filter.Constants):
        model = OapPropEditClassesListDB


class OapPropEditClassesListCreate(BaseModel):
    program_id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class OapPropEditClassesListUpdate(OapPropEditClassesListCreate):
    id: int


class OapPropEditClassesListOut(OapPropEditClassesListUpdate):
    pass


class OapPropEditClassesListWithItemsOut(OapPropEditClassesListUpdate):
    ref_items: list[OapPropEditClassesItemOut]
