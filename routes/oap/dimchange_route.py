from fastapi import APIRouter, Depends
from fastapi_filter import FilterDepends
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import delete, select
from sqlalchemy.orm import Session
from api_models.oap.dimchange import (
    OapDimChangeFilter,
    OapDimChangeOut,
    OapDimChangeCreate,
    OapDimChangeUpdate,
)
from api_models.util.model_scheme import get_simple_model_scheme
from models import generate_session
from models.oap import OapActionDB, OapDimChangeDB
from sqlalchemy.orm import joinedload
from fastapi_pagination import Page
from routes import util
from sqlalchemy.orm import joinedload, selectinload

from sqlalchemy import select, func

router = APIRouter(prefix="/dimchange")

@router.get("/scheme")
def read_scheme(extensive: bool = False):
    """
    return dimchange scheme
    """
    scheme =  OapDimChangeOut.model_json_schema() if extensive else get_simple_model_scheme(OapDimChangeOut)
    return scheme

@router.get("/{dimchange_id}", response_model=OapDimChangeOut)
def read_dimchange(
    dimchange_id: int,
    session: Session = Depends(generate_session),
):
    """
    return dimchange by id
    """
    select_stmt = select(OapDimChangeDB).filter(OapDimChangeDB.id == dimchange_id)
    item = session.execute(select_stmt).scalar_one()
    return item


@router.get("")
def read_dimchanges(
    session: Session = Depends(generate_session),
    dimchange_filter=FilterDepends(OapDimChangeFilter),
) -> Page[OapDimChangeOut]:
    """
    return all dimchange
    """
    return paginate(session, dimchange_filter.filter(select(OapDimChangeDB)))


@router.put("")
def update_dimchange(
    dimchange: OapDimChangeUpdate,
    session: Session = Depends(generate_session),
):
    """
    update dimchange
    """
    return util.exec_simple_update(OapDimChangeDB, session, dimchange)


@router.delete("/{dimchange_id}")
def delete_dimchange(
    dimchange_id: int,
    session: Session = Depends(generate_session),
):
    """
    delete dimchange
    """
    return util.exec_simple_delete(OapDimChangeDB, session, dimchange_id)


@router.post("")
def create_dimchange(
    dimchange: OapDimChangeCreate, session: Session = Depends(generate_session)
):
    """
    create dimchange
    """
    return util.exec_simple_insert(OapDimChangeDB, session, dimchange)
