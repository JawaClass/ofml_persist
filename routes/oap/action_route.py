from fastapi import APIRouter, Depends
from fastapi_filter import FilterDepends
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import delete, insert, select
from sqlalchemy.orm import Session
from api_models.oap.action import (
    OapActionCreate,
    OapActionFilter,
    OapActionMethodCallOut, 
    OapActionOut,
    OapActionItemOut,
    OapActionUpdate,
    OapActionWithObjectsOut,
)
from api_models.oap.object import OapObjectOut
from api_models.util.model_scheme import get_simple_model_scheme
from models import generate_session
from models.oap import ActionType, OapActionDB, OapObjectDB, oap_action_object_association_table
from sqlalchemy.orm import joinedload
from fastapi_pagination import Page
from routes import util
from sqlalchemy.orm import joinedload, selectinload

from sqlalchemy import select, func

from routes.pagination import LargePage

router = APIRouter(prefix="/action")

@router.get("/scheme")
def read_scheme(extensive: bool = False):
    """
    return action scheme
    """
    scheme =  OapActionOut.model_json_schema() if extensive else get_simple_model_scheme(OapActionOut)
    return scheme


@router.get("/methodcalls")
def read_actions_methodcalls(
    session: Session = Depends(generate_session),
    action_filter=FilterDepends(OapActionFilter),
) -> LargePage[OapActionMethodCallOut]:
    """
    return all actions with methodcall
    """
    return paginate(session, action_filter.filter(
        select(OapActionDB)
        .options(selectinload(OapActionDB.ref_methodcall))
        .filter(OapActionDB.type == ActionType.MethodCall))
    )

@router.delete("/{action_id}/objects/{object_id}")
def delete_object_by_id(
    action_id: int, object_id: int, session: Session = Depends(generate_session)
) -> int:
    """
    delete object relationship by id
    """
    delete_stmt = delete(oap_action_object_association_table).filter(
        oap_action_object_association_table.c.oap_action_id == action_id,
        oap_action_object_association_table.c.oap_object_id == object_id,
    )
    result = session.execute(delete_stmt)
    session.commit()
    return result.rowcount


@router.post("/{action_id}/objects/{object_id}")
def add_object_by_id(
    action_id: int, object_id: int, session: Session = Depends(generate_session)
) -> int:
    """
    add object relationship by id
    """
    insert_stmt = insert(oap_action_object_association_table).values(
        oap_action_id=action_id,
        oap_object_id=object_id,
    )
    result = session.execute(insert_stmt)
    session.commit()
    return result.rowcount


@router.get("/{action_id}/objects", response_model=OapActionWithObjectsOut)
def read_action_objects(
    action_id: int,
    session: Session = Depends(generate_session),
):
    """
    return action objects by id
    """
    select_stmt = (
        select(OapActionDB)
        .options(selectinload(OapActionDB.ref_objects))
        .filter(OapActionDB.id == action_id)
    )
    item = session.execute(select_stmt).scalar_one()
    return item


@router.get("/{action_id}", response_model=OapActionOut)
def read_action(
    action_id: int,
    session: Session = Depends(generate_session),
):
    """
    return action by id
    """
    select_stmt = select(OapActionDB).filter(OapActionDB.id == action_id)
    item = session.execute(select_stmt).scalar_one()
    return item


@router.get("/{action_id}/item", response_model=OapActionItemOut)
def read_action_item(
    action_id: int,
    session: Session = Depends(generate_session),
):
    """
    return action itemby id
    """
    select_stmt = select(OapActionDB).filter(OapActionDB.id == action_id)
    item = session.execute(select_stmt).scalar_one()
    return item

@router.get("")
def read_actions(
    session: Session = Depends(generate_session),
    action_filter=FilterDepends(OapActionFilter),
) -> LargePage[OapActionOut]:
    """
    return all actions
    """
    return paginate(session, action_filter.filter(select(OapActionDB)))
 

@router.post("")
def create_action(
    action: OapActionCreate, session: Session = Depends(generate_session)
):
    """
    create action
    """
    return util.exec_simple_insert(OapActionDB, session, action)


@router.put("")
def update_action(
    action: OapActionUpdate,
    session: Session = Depends(generate_session),
):
    """
    update action
    """
    return util.exec_simple_update(OapActionDB, session, action)


@router.delete("/{action_id}")
def delete_action(
    action_id: int,
    session: Session = Depends(generate_session),
):
    """
    delete action
    """
    return util.exec_simple_delete(OapActionDB, session, action_id)
