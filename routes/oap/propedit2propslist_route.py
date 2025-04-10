from fastapi import APIRouter, Depends
from fastapi_filter import FilterDepends
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import delete, select
from sqlalchemy.orm import Session
from api_models.oap.propeditprops import (
    OapPropEditPropsListCreate,
    OapPropEditPropsListFilter,
    OapPropEditPropsListOut,
    OapPropEditPropsListUpdate,
    OapPropEditPropsListWithItemsOut,
)
from api_models.util.model_scheme import get_simple_model_scheme
from models import generate_session
from models.oap import OapPropEditPropsItemDB, OapPropEditPropsListDB
from sqlalchemy.orm import joinedload
from fastapi_pagination import Page
from routes import util
from sqlalchemy.orm import joinedload, selectinload

from sqlalchemy import select, func

router = APIRouter(prefix="/propedit2propslist")


@router.get("/scheme")
def read_scheme(extensive: bool = False):
    """
    return propedit2propslist scheme
    """
    scheme =  OapPropEditPropsListOut.model_json_schema() if extensive else get_simple_model_scheme(OapPropEditPropsListOut)
    return scheme


@router.get("/{list_id}/items", response_model=OapPropEditPropsListWithItemsOut)
def read_list_items(
    list_id: int,
    session: Session = Depends(generate_session),
):
    """
    return list items by id
    """
    select_stmt = (
        select(OapPropEditPropsListDB)
        .options(selectinload(OapPropEditPropsListDB.ref_items))
        .filter(OapPropEditPropsListDB.id == list_id)
    )
    item = session.execute(select_stmt).scalar_one()
    return item


@router.get("/{list_id}", response_model=OapPropEditPropsListOut)
def read_list(
    list_id: int,
    session: Session = Depends(generate_session),
):
    """
    return propedit2propslist by id
    """
    select_stmt = select(OapPropEditPropsListDB).filter(
        OapPropEditPropsListDB.id == list_id
    )
    item = session.execute(select_stmt).scalar_one()
    return item


@router.get("")
def read_lists(
    session: Session = Depends(generate_session),
    list_filter=FilterDepends(OapPropEditPropsListFilter),
) -> Page[OapPropEditPropsListOut]:
    """
    return all propedit2propslist
    """
    return paginate(session, list_filter.filter(select(OapPropEditPropsListDB)))


@router.put("")
def update_list(
    list_: OapPropEditPropsListUpdate,
    session: Session = Depends(generate_session),
):
    """
    update propedit2propslist
    """
    return util.exec_simple_update(OapPropEditPropsListDB, session, list_)


@router.delete("/{list_id}")
def delete_list(
    list_id: int,
    session: Session = Depends(generate_session),
):
    """
    delete propedit2propslist
    """
    print("propedit2propslist::delete_list", list_id)
    return util.exec_simple_delete(OapPropEditPropsListDB, session, list_id)


@router.post("")
def create_list(
    list_: OapPropEditPropsListCreate, session: Session = Depends(generate_session)
):
    """
    create list
    """ 
    return util.exec_simple_insert(OapPropEditPropsListDB, session, list_)
