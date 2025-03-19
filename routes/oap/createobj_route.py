from fastapi import APIRouter, Depends
from fastapi_filter import FilterDepends
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import delete, select
from sqlalchemy.orm import Session
from api_models.oap.createobj import (
    OapCreateObjCreate,
    OapCreateObjFilter,
    OapCreateObjOut,
    OapCreateObjUpdate,
)
from api_models.util.model_scheme import get_simple_model_scheme
from models import generate_session
from models.oap import OapCreateObjDB
from sqlalchemy.orm import joinedload
from fastapi_pagination import Page
from routes import util
from sqlalchemy.orm import joinedload, selectinload

from sqlalchemy import select, func

router = APIRouter(prefix="/createobj")

@router.get("/scheme")
def read_scheme(extensive: bool = False):
    """
    return createobj scheme
    """
    scheme =  OapCreateObjOut.model_json_schema() if extensive else get_simple_model_scheme(OapCreateObjOut)
    return scheme

@router.get("/{createobj_id}", response_model=OapCreateObjOut)
def read_createobj(
    createobj_id: int,
    session: Session = Depends(generate_session),
):
    """
    return createobj by id
    """
    select_stmt = (
        select(OapCreateObjDB)
        .options(selectinload(OapCreateObjDB.ref_parent))
        .filter(OapCreateObjDB.id == createobj_id)
    )
    item = session.execute(select_stmt).scalar_one()
    return item


@router.get("")
def read_createobjects(
    session: Session = Depends(generate_session),
    createobj_filter=FilterDepends(OapCreateObjFilter),
) -> Page[OapCreateObjOut]:
    """
    return all createobj
    """
    return paginate(session, createobj_filter.filter(select(OapCreateObjDB)))


@router.put("")
def update_createobj(
    createobj: OapCreateObjUpdate,
    session: Session = Depends(generate_session),
):
    """
    update createobj
    """
    return util.exec_simple_update(OapCreateObjDB, session, createobj)


@router.delete("/{createobj_id}")
def delete_createobj(
    createobj_id: int,
    session: Session = Depends(generate_session),
):
    """
    delete createobj
    """
    return util.exec_simple_delete(OapCreateObjDB, session, createobj_id)


@router.post("")
def create_createobj(
    createobj: OapCreateObjCreate, session: Session = Depends(generate_session)
):
    """
    create createobj
    """
    return util.exec_simple_insert(OapCreateObjDB, session, createobj)
