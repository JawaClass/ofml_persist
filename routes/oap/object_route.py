from fastapi import APIRouter, Depends
from fastapi_filter import FilterDepends
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import delete, select
from sqlalchemy.orm import Session
from api_models.oap.object import (
    OapObjectCreate,
    OapObjectOut,
    OapObjectFilter,
    OapObjectUpdate,
)
from api_models.util.model_scheme import get_simple_model_scheme
from models import generate_session
from sqlalchemy.orm import joinedload
from fastapi_pagination import Page
from models.oap import OapObjectDB
from routes import util
from sqlalchemy.orm import joinedload, selectinload

from sqlalchemy import select, func

router = APIRouter(prefix="/object")


@router.get("/scheme")
def read_scheme(extensive: bool = False):
    """
    return object scheme
    """
    scheme =  OapObjectOut.model_json_schema() if extensive else get_simple_model_scheme(OapObjectOut)
    return scheme

@router.get("/{object_id}", response_model=OapObjectOut)
def read_object(
    object_id: int,
    session: Session = Depends(generate_session),
):
    """
    return object by id
    """
    select_stmt = select(OapObjectDB).filter(OapObjectDB.id == object_id)
    item = session.execute(select_stmt).scalar_one()
    return item


@router.get("")
def read_objects(
    session: Session = Depends(generate_session),
    object_filter=FilterDepends(OapObjectFilter),
) -> Page[OapObjectOut]:
    """
    return all objects
    """
    return paginate(session, object_filter.filter(select(OapObjectDB)))


@router.put("")
def update_object(
    object: OapObjectUpdate,
    session: Session = Depends(generate_session),
):
    """
    update object
    """
    return util.exec_simple_update(OapObjectDB, session, object)


@router.delete("/{object_id}")
def delete_object(
    object_id: int,
    session: Session = Depends(generate_session),
):
    """
    delete object
    """
    return util.exec_simple_delete(OapObjectDB, session, object_id)


@router.post("")
def create_object(
    object: OapObjectCreate, session: Session = Depends(generate_session)
):
    """
    create object
    """
    return util.exec_simple_insert(OapObjectDB, session, object)
