from __future__ import annotations

from fastapi import APIRouter, Depends
from fastapi_filter import FilterDepends
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import delete, select
from sqlalchemy.orm import Session
from api_models.oap.action import OapActionOut
from api_models.oap.actionlist import (
    OapActionListCreate,
    OapActionListItemsOut,
    OapActionListUpdate,
    OapActionListOut,
    OapActionListListFilter,
)
from api_models.util.model_scheme import get_simple_model_scheme
from models import generate_session
from models.oap import OapActionListItemDB, OapActionListListDB
from sqlalchemy.orm import joinedload
from fastapi_pagination import Page
from routes import util
from sqlalchemy.orm import joinedload, selectinload

from sqlalchemy import select, func

from routes.pagination import LargePage

router = APIRouter(prefix="/actionlist")


@router.get("/scheme")
def read_scheme(extensive: bool = False):
    """
    return actionlistheader scheme
    """
    scheme =  OapActionListOut.model_json_schema() if extensive else get_simple_model_scheme(OapActionListOut)
    return scheme

@router.get("/{actionlist_id}", response_model=OapActionListItemsOut)
def read_actionlist(
    actionlist_id: int,
    session: Session = Depends(generate_session),
):
    """
    return actionlist by id
    """
    select_stmt = (
        select(OapActionListListDB)
        .options(
            selectinload(OapActionListListDB.ref_actionlist).selectinload(
                OapActionListItemDB.actions
            )
        )
        .filter(OapActionListListDB.id == actionlist_id)
    )
    item = session.execute(select_stmt).scalar_one()
    return item

@router.get("")
def read_actionlists(
    session: Session = Depends(generate_session),
    actionlist_filter=FilterDepends(OapActionListListFilter),
) -> LargePage[OapActionListOut]:
    """
    return all actionlist
    """
    return paginate(session, actionlist_filter.filter(select(OapActionListListDB)))


@router.put("")
def update_actionlist(
    actionlist: OapActionListUpdate,
    session: Session = Depends(generate_session),
):
    """
    update actionlist
    """
    return util.exec_simple_update(OapActionListListDB, session, actionlist)


@router.delete("/{actionlist_id}")
def delete_actionlist(
    actionlist_id: int,
    session: Session = Depends(generate_session),
):
    """
    delete actionlist
    """
    return util.exec_simple_delete(OapActionListListDB, session, actionlist_id)


@router.post("", response_model=OapActionListItemsOut)
def create_actionlist(
    actionlist: OapActionListCreate, session: Session = Depends(generate_session)
):
    """
    create actionlist
    """
    return util.exec_simple_insert(OapActionListListDB, session, actionlist)
