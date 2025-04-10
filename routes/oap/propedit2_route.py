from fastapi import APIRouter, Depends
from fastapi_filter import FilterDepends
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import delete, select
from sqlalchemy.orm import Session
from api_models.oap.propedit2 import (
    OapPropEdit2Filter,
    OapPropEdit2ItemOut,
    OapPropEdit2Out,
    OapPropEdit2Update,
    OapPropEdit2Create,
)
from api_models.util.model_scheme import get_simple_model_scheme
from models import generate_session
from models.oap import OapPropEdit2DB
from sqlalchemy.orm import joinedload
from fastapi_pagination import Page
from routes import util
from sqlalchemy.orm import joinedload, selectinload

from sqlalchemy import select, func

router = APIRouter(prefix="/propedit2")


@router.get("/scheme")
def read_scheme(extensive: bool = False):
    """
    return propedit2 scheme
    """
    scheme =  OapPropEdit2Out.model_json_schema() if extensive else get_simple_model_scheme(OapPropEdit2Out)
    return scheme

@router.get("/{propedit2_id}/item", response_model=OapPropEdit2ItemOut)
@router.get("/{propedit2_id}", response_model=OapPropEdit2ItemOut)
def read_propedit2(
    propedit2_id: int,
    session: Session = Depends(generate_session),
):
    """
    return propedit2 by id
    """
    select_stmt = select(OapPropEdit2DB).filter(OapPropEdit2DB.id == propedit2_id)
    item = session.execute(select_stmt).scalar_one()
    return item


@router.get("")
def read_propedit2s(
    session: Session = Depends(generate_session),
    propedit2_filter=FilterDepends(OapPropEdit2Filter),
) -> Page[OapPropEdit2Out]:
    """
    return all propedit2s
    """
    return paginate(session, propedit2_filter.filter(select(OapPropEdit2DB)))


@router.put("")
def update_propedit2(
    methodcall: OapPropEdit2Update,
    session: Session = Depends(generate_session),
):
    """
    update propedit2
    """
    return util.exec_simple_update(OapPropEdit2DB, session, methodcall)


@router.delete("/{propedit2_id}")
def delete_propedit2(
    propedit2_id: int,
    session: Session = Depends(generate_session),
):
    """
    delete propedit2
    """
    return util.exec_simple_delete(OapPropEdit2DB, session, propedit2_id)


@router.post("")
def create_propedit2(
    propedit2: OapPropEdit2Create, session: Session = Depends(generate_session)
):
    """
    create propedit2
    """
    return util.exec_simple_insert(OapPropEdit2DB, session, propedit2)
