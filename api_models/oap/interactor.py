from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field
from fastapi_filter.contrib.sqlalchemy import Filter
from api_models.oap import OapBaseFilter
from api_models.oap.action import OapActionItemOut, OapActionOut
from api_models.oap.symboldisplay import OapSymbolDisplayItemOut
from models.oap import OapInteractorDB, SymbolSize, SymbolType


class OapInteractorFilter(OapBaseFilter):

    class Constants(Filter.Constants):
        model = OapInteractorDB


class OapInteractorCreate(BaseModel):
    program_id: int
    name: str
    condition: str | None = None
    needs_plan_mode: str | None = None
    symbol_type: SymbolType
    symbol_size: SymbolSize
    model_config = ConfigDict(from_attributes=True)


class OapInteractorUpdate(OapInteractorCreate):
    id: int


class OapInteractorOut(OapInteractorUpdate):
    pass


class OapInteractorActionAssocOut(BaseModel):
    position: int
    ref_action: OapActionOut


class OapInteractorItemOut(OapInteractorUpdate):
    # ref_actions: list[OapInteractorActionAssocOut]
    # actions: list[OapActionOut]  
    actions: list[OapActionItemOut]
    # old ActionItemOut...
    ref_symboldisplays: list[OapSymbolDisplayItemOut]

OapInteractorItemOut.model_rebuild()

class OapInteractorAddActionUpdate(BaseModel): 
    position_idx: int
