from __future__ import annotations

from builtins import list
from pydantic import BaseModel, ConfigDict, Field
from fastapi_filter.contrib.sqlalchemy import Filter
from api_models.oap import OapBaseFilter
from api_models.oap.createobj import OapCreateObjOut
from api_models.oap.dimchange import OapDimChangeOut
from api_models.oap.extmedia import OapExtMediaOut
from api_models.oap.message import OapMessageOut
from api_models.oap.methodcall import OapMethodCallOut
from api_models.oap.object import OapObjectOut
from api_models.oap.propchange import OapPropChangeOut
from api_models.oap.propedit import OapPropEditOut
from api_models.oap.propedit2 import OapPropEdit2Out
from models.oap import ActionType, OapActionDB


from typing import TYPE_CHECKING, Any, Optional

from api_models.oap.actionchoice import OapActionChoiceItemOut, OapActionChoiceOut
    


class OapActionFilter(OapBaseFilter):

    type: ActionType | None = None

    class Constants(Filter.Constants):
        model = OapActionDB


class OapActionCreate(BaseModel):
    program_id: int
    name: str
    condition: str | None = None
    type: ActionType
    message_id: int | None = None
    dimchange_id: int | None = None
    propchange_id: int | None = None
    propedit2_id: int | None = None
    propedit_id: int | None = None
    extmedia_id: int | None = None
    createobj_id: int | None = None
    methodcall_id: int | None = None
    actionchoice_id: int | None = None

    model_config = ConfigDict(from_attributes=True)


class OapActionUpdate(OapActionCreate):
    id: int


class OapActionOut(OapActionUpdate):
    pass


class OapActionMethodCallOut(OapActionOut):
    ref_methodcall: OapMethodCallOut | None = None


class OapActionWithObjectsOut(OapActionOut):
    ref_objects: list[OapObjectOut] = []


class OapActionItemOut(OapActionOut):

    ref_message: OapMessageOut | None = None
    ref_dimchange: OapDimChangeOut | None = None
    ref_propchange: OapPropChangeOut | None = None
    ref_propedit2: OapPropEdit2Out | None = None
    ref_propedit: OapPropEditOut | None = None
    ref_extmedia: OapExtMediaOut | None = None
    ref_createobj: OapCreateObjOut | None = None
    ref_methodcall: OapMethodCallOut | None = None
    ref_actionchoice: OapActionChoiceItemOut | None = None
    ref_objects: list[OapObjectOut] = []

# OapActionItemOut.model_rebuild() 