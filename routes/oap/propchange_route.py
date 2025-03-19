from fastapi import APIRouter, Depends
from fastapi_filter import FilterDepends
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import delete, select
from sqlalchemy.orm import Session
from api_models.oap.propchange import (
    OapPropChangeCreate,
    OapPropChangeOut,
    OapPropChangeFilter,
    OapPropChangeUpdate,
)
from api_models.util.model_scheme import get_simple_model_scheme
from models import generate_session
from sqlalchemy.orm import joinedload
from fastapi_pagination import Page
from models.oap import OapPropChangeDB
from routes import util
from sqlalchemy.orm import joinedload, selectinload

from sqlalchemy import select, func

router = APIRouter(prefix="/propchange")


@router.get("/scheme")
def read_scheme(extensive: bool = False):
    """
    return propchange scheme
    """
    scheme =  OapPropChangeOut.model_json_schema() if extensive else get_simple_model_scheme(OapPropChangeOut)
    return scheme

@router.get("/{propchange_id}", response_model=OapPropChangeOut)
def read_propchange(
    propchange_id: int,
    session: Session = Depends(generate_session),
):
    """
    return propchange by id
    """
    select_stmt = select(OapPropChangeDB).filter(OapPropChangeDB.id == propchange_id)
    item = session.execute(select_stmt).scalar_one()
    return item


@router.get("")
def read_propchanges(
    session: Session = Depends(generate_session),
    propchange_filter=FilterDepends(OapPropChangeFilter),
) -> Page[OapPropChangeOut]:
    """
    return all propchanges
    """
    return paginate(session, propchange_filter.filter(select(OapPropChangeDB)))


@router.put("")
def update_propchange(
    propchange: OapPropChangeUpdate,
    session: Session = Depends(generate_session),
):
    """
    update propchange
    """
    return util.exec_simple_update(OapPropChangeDB, session, propchange)


@router.delete("/{propchange_id}")
def delete_propchange(
    propchange_id: int,
    session: Session = Depends(generate_session),
):
    """
    delete propchange
    """
    return util.exec_simple_delete(OapPropChangeDB, session, propchange_id)


@router.post("")
def create_propchange(
    propchange: OapPropChangeCreate, session: Session = Depends(generate_session)
):
    """
    create propchange
    """
    return util.exec_simple_insert(OapPropChangeDB, session, propchange)
