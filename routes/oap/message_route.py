from fastapi import APIRouter, Depends
from fastapi_filter import FilterDepends
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import delete, select
from sqlalchemy.orm import Session
from api_models.oap.message import (
    OapMessageCreate,
    OapMessageFilter,
    OapMessageOut,
    OapMessageUpdate,
)
from api_models.util.model_scheme import get_simple_model_scheme
from models import generate_session
from models.oap import OapActionDB, OapMessageDB
from sqlalchemy.orm import joinedload
from fastapi_pagination import Page
from routes import util
from sqlalchemy.orm import joinedload, selectinload

from sqlalchemy import select, func

router = APIRouter(prefix="/message")

 
@router.get("/scheme")
def read_scheme(extensive: bool = False):
    """
    return message scheme
    """
    scheme =  OapMessageOut.model_json_schema() if extensive else get_simple_model_scheme(OapMessageOut)
    return scheme

@router.get("/{message_id}", response_model=OapMessageOut)
def read_message(
    message_id: int,
    session: Session = Depends(generate_session),
):
    """
    return message by id
    """
    select_stmt = select(OapMessageDB).filter(OapMessageDB.id == message_id)
    item = session.execute(select_stmt).scalar_one()
    return item


@router.get("")
def read_messages(
    session: Session = Depends(generate_session),
    message_filter=FilterDepends(OapMessageFilter),
) -> Page[OapMessageOut]:
    """
    return all message
    """
    return paginate(session, message_filter.filter(select(OapMessageDB)))


@router.put("")
def update_message(
    message: OapMessageUpdate,
    session: Session = Depends(generate_session),
):
    """
    update message
    """
    return util.exec_simple_update(OapMessageDB, session, message)


@router.delete("/{message_id}")
def delete_message(
    message_id: int,
    session: Session = Depends(generate_session),
):
    """
    delete message
    """
    return util.exec_simple_delete(OapMessageDB, session, message_id)


@router.post("")
def create_message(
    message: OapMessageCreate, session: Session = Depends(generate_session)
):
    """
    create message
    """
    return util.exec_simple_insert(OapMessageDB, session, message)
