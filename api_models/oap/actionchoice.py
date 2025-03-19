from pydantic import BaseModel, ConfigDict
from fastapi_filter.contrib.sqlalchemy import Filter
from api_models.oap import OapBaseFilter
from api_models.oap.actionlist import OapActionListItemsOut
from api_models.oap.text import OapTextOut
from models.oap import ActionChoiceTileSize, ActionChoiceViewType, OapActionChoiceDB


class OapActionChoiceFilter(OapBaseFilter):
    view_type: ActionChoiceViewType | None = None

    class Constants(Filter.Constants):
        model = OapActionChoiceDB


class OapActionChoiceCreate(BaseModel):
    program_id: int
    name: str
    title_id: int | None = None
    actionlist_id: int | None = None
    view_type: ActionChoiceViewType
    argument: ActionChoiceTileSize | None = None

    model_config = ConfigDict(from_attributes=True)


class OapActionChoiceUpdate(OapActionChoiceCreate):
    id: int


class OapActionChoiceOut(OapActionChoiceUpdate):
    pass

class OapActionChoiceItemOut(OapActionChoiceOut):
    ref_actionlistlist: OapActionListItemsOut | None = None
    ref_title: OapTextOut | None = None