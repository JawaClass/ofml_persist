from __future__ import annotations
from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field
from fastapi_filter.contrib.sqlalchemy import Filter

from api_models.oap import OapBaseFilter
from api_models.oap.image import OapImageOut
from api_models.oap.text import OapTextOut
from models.oap import OapActionListListDB, OapActionListItemDB


if TYPE_CHECKING:
    from api_models.oap.action import OapActionOut

# Item
class OapActionListItemFilter(OapBaseFilter):

    class Constants(Filter.Constants):
        model = OapActionListItemDB


class OapActionListItemCreate(BaseModel):
    program_id: int
    actionlistlist_id: int
    position: int
    condition: str | None = None
    text_id: int | None = None
    image_id: int | None = None


class OapActionListItemUpdate(OapActionListItemCreate):
    id: int


class OapActionListItemOut(OapActionListItemUpdate):
    pass

class OapActionListItemItemOut(OapActionListItemOut):
    ref_text: OapTextOut | None = None
    ref_image: OapImageOut | None = None
    actions: list[OapActionOut]

# OapActionListItemItemOut.model_rebuild()

# List


class OapActionListListFilter(OapBaseFilter):
    name: str | None = None

    class Constants(Filter.Constants):
        model = OapActionListListDB


class OapActionListCreate(BaseModel):
    program_id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class OapActionListUpdate(OapActionListCreate):
    id: int


class OapActionListOut(OapActionListUpdate):
    # ref_actionlist: list[OapActionListItemOut]
    pass

class OapActionListItemsOut(OapActionListUpdate):
    ref_actionlist: list[OapActionListItemItemOut]

class OapActionListAddActionUpdate(BaseModel):
    action_id: int
    position_idx: int


class OapActionListActionUpdate(BaseModel):
    position_idx: int
