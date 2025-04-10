from fastapi import APIRouter, Depends
from fastapi_filter import FilterDepends
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import delete, insert, select, update, func
from sqlalchemy.orm import Session
from api_models.oap.actionlist import (
    OapActionListActionUpdate,
    OapActionListAddActionUpdate,
    OapActionListItemCreate,
    OapActionListItemItemOut,
    OapActionListItemUpdate,
    OapActionListItemOut,
    OapActionListItemFilter,
)
from api_models.util.model_scheme import get_simple_model_scheme
from models import generate_session
from models.oap import OapActionListActionAssocDB, OapActionListItemDB
from sqlalchemy.orm import joinedload
from fastapi_pagination import Page
from routes import util
from sqlalchemy.orm import joinedload, selectinload

from sqlalchemy import select, func

from routes.pagination import LargePage

router = APIRouter(prefix="/actionlistitem")


@router.get("/scheme")
def read_scheme(extensive: bool = False):
    """
    return actionlistitem scheme
    """
    scheme =  OapActionListItemOut.model_json_schema() if extensive else get_simple_model_scheme(OapActionListItemOut)
    return scheme

@router.put("/{listitem_id}/actions/{action_id}")
def update_action_by_id(
    listitem_id: int,
    action_id: int,
    action_update: OapActionListActionUpdate,
    session: Session = Depends(generate_session),
) -> int:
    """
    update action relationship by id
    """
    update_stmt = (
        update(OapActionListActionAssocDB)
        .filter(
            OapActionListActionAssocDB.actionlist_id == listitem_id,
            OapActionListActionAssocDB.action_id == action_id,
        )
        .values(position=action_update.position_idx)
    )
    result = session.execute(update_stmt)
    session.commit()
    return result.rowcount


@router.post("/{listitem_id}/actions/{action_id}")
def add_action_by_id(
    listitem_id: int,
    action_id: int,
    add_action_update: OapActionListAddActionUpdate,
    session: Session = Depends(generate_session),
) -> int:
    """
    add action relationship by id and position index
    """
    if add_action_update.position_idx is None: 
        # get the current largest position index inside this items ActionList
        stmt = select(func.max(OapActionListActionAssocDB.position)).where(
            OapActionListActionAssocDB.actionlist_id == listitem_id
            )
        max_position = session.execute(stmt).scalar()
        position_idx = max_position + 1 if max_position is not None else 0
    else:
        position_idx = add_action_update.position_idx

    insert_stmt = insert(OapActionListActionAssocDB).values(
        actionlist_id=listitem_id,
        action_id=action_id,
        position=position_idx,
    )

    result = session.execute(insert_stmt)
    session.commit()
    return result.rowcount


@router.delete("/{listitem_id}/actions/{action_id}")
def delete_action_by_id(
    listitem_id: int, action_id: int, session: Session = Depends(generate_session)
) -> int:
    """
    delete action relationship by id
    """
    delete_stmt = delete(OapActionListActionAssocDB).filter(
        OapActionListActionAssocDB.actionlist_id == listitem_id,
        OapActionListActionAssocDB.action_id == action_id,
    )
    result = session.execute(delete_stmt)
    session.commit()
    return result.rowcount


@router.get("/{actionlistitem_id}", response_model=OapActionListItemItemOut)
def read_actionlistitem(
    actionlistitem_id: int,
    session: Session = Depends(generate_session),
):
    """
    return actionlistitem by id
    """
    select_stmt = select(OapActionListItemDB).filter(
        OapActionListItemDB.id == actionlistitem_id
    )
    item = session.execute(select_stmt).scalar_one()
    return item

@router.get("")
def read_actionlistitems(
    session: Session = Depends(generate_session),
    actionlistitem_filter=FilterDepends(OapActionListItemFilter),
) -> LargePage[OapActionListItemOut]:
    """
    return all actionlistitem
    """
    return paginate(session, actionlistitem_filter.filter(select(OapActionListItemDB)))
  
@router.put("")
def update_actionlistitem(
    actionlistitem: OapActionListItemUpdate,
    session: Session = Depends(generate_session),
):
    """
    update actionlistitem
    """
    return util.exec_simple_update(OapActionListItemDB, session, actionlistitem)


@router.delete("/{actionlistitem_id}")
def delete_actionlistitem(
    actionlistitem_id: int,
    session: Session = Depends(generate_session),
):
    """
    delete actionlistitem
    """
    return util.exec_simple_delete(OapActionListItemDB, session, actionlistitem_id)


@router.post("", response_model=OapActionListItemOut)
def create_actionlistitem(
    actionlistitem: OapActionListItemCreate,
    session: Session = Depends(generate_session),
):
    """
    create actionlistitem
    """
    return util.exec_simple_insert(OapActionListItemDB, session, actionlistitem)
