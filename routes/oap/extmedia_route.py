from fastapi import APIRouter, Depends
from fastapi_filter import FilterDepends
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import delete, select
from sqlalchemy.orm import Session
from api_models.oap.extmedia import (
    OapExtMediaCreate,
    OapExtMediaOut,
    OapExtMediaFilter,
    OapExtMediaUpdate,
)
from api_models.util.model_scheme import get_simple_model_scheme
from models import generate_session
from sqlalchemy.orm import joinedload
from fastapi_pagination import Page
from models.oap import OapExtMediaDB
from routes import util
from sqlalchemy.orm import joinedload, selectinload

from sqlalchemy import select, func

router = APIRouter(prefix="/extmedia")


@router.get("/scheme")
def read_scheme(extensive: bool = False):
    """
    return extmedia scheme
    """
    scheme =  OapExtMediaOut.model_json_schema() if extensive else get_simple_model_scheme(OapExtMediaOut)
    return scheme

@router.get("/{extmedia_id}", response_model=OapExtMediaOut)
def read_extmedia(
    extmedia_id: int,
    session: Session = Depends(generate_session),
):
    """
    return extmedia by id
    """
    select_stmt = select(OapExtMediaDB).filter(OapExtMediaDB.id == extmedia_id)
    item = session.execute(select_stmt).scalar_one()
    return item



@router.get("")
def read_extmedias(
    session: Session = Depends(generate_session),
    extmedia_filter=FilterDepends(OapExtMediaFilter),
) -> Page[OapExtMediaOut]:
    """
    return all extmedia
    """
    return paginate(session, extmedia_filter.filter(select(OapExtMediaDB)))


@router.put("")
def update_extmedia(
    extmedia: OapExtMediaUpdate,
    session: Session = Depends(generate_session),
):
    """
    update extmedia
    """
    return util.exec_simple_update(OapExtMediaDB, session, extmedia)


@router.delete("/{extmedia_id}")
def delete_extmedia(
    extmedia_id: int,
    session: Session = Depends(generate_session),
):
    """
    delete extmedia
    """
    return util.exec_simple_delete(OapExtMediaDB, session, extmedia_id)


@router.post("")
def create_extmedia(extmedia: OapExtMediaCreate, session: Session = Depends(generate_session)):
    """
    create extmedia
    """
    return util.exec_simple_insert(OapExtMediaDB, session, extmedia)
