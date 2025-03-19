from fastapi import APIRouter, Depends
from fastapi_filter import FilterDepends
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import delete, select
from sqlalchemy.orm import Session
from api_models.oap.propedit import (
    OapPropEditCreate,
    OapPropEditItemOut,
    OapPropEditOut,
    OapPropEditFilter,
    OapPropEditUpdate,
)
from api_models.util.model_scheme import get_simple_model_scheme
from models import generate_session
from sqlalchemy.orm import joinedload
from fastapi_pagination import Page
from models.oap import OapPropEditDB
from routes import util
from sqlalchemy.orm import joinedload, selectinload

from sqlalchemy import select, func

from routes.pagination import LargePage

router = APIRouter(prefix="/propedit")


@router.get("/scheme")
def read_scheme(extensive: bool = False):
    """
    return propedit scheme
    """
    scheme =  OapPropEditOut.model_json_schema() if extensive else get_simple_model_scheme(OapPropEditOut)
    return scheme


@router.get("/{propedit_id}/item", response_model=OapPropEditItemOut)
@router.get("/{propedit_id}", response_model=OapPropEditItemOut)
def read_propedit(
    propedit_id: int,
    session: Session = Depends(generate_session),
):
    """
    return propedit by id
    """
    select_stmt = select(OapPropEditDB).filter(OapPropEditDB.id == propedit_id)
    item = session.execute(select_stmt).scalar_one()
    return item


@router.get("")
def read_propedits(
    session: Session = Depends(generate_session),
    propedit_filter=FilterDepends(OapPropEditFilter),
) -> LargePage[OapPropEditOut]:
    """
    return all propedits
    """
    return paginate(session, propedit_filter.filter(select(OapPropEditDB)))


@router.put("")
def update_propedit(
    propedit: OapPropEditUpdate,
    session: Session = Depends(generate_session),
):
    """
    update propedit
    """
    return util.exec_simple_update(OapPropEditDB, session, propedit)


@router.delete("/{propedit_id}")
def delete_propedit(
    propedit_id: int,
    session: Session = Depends(generate_session),
):
    """
    delete propedit
    """
    return util.exec_simple_delete(OapPropEditDB, session, propedit_id)


@router.post("")
def create_propedit(
    propedit: OapPropEditCreate, session: Session = Depends(generate_session)
):
    """
    create propedit
    """
    return util.exec_simple_insert(OapPropEditDB, session, propedit)


# @router.get("")
# def read_propedits(
#     session: Session = Depends(generate_session),
#     propedit_filter=FilterDepends(OapPropEditFilter),
# ) -> Page[OapPropEditOut]:
#     """
#     return all propedits
#     """
#     return paginate(session, propedit_filter.filter(select(OapPropEditDB)))