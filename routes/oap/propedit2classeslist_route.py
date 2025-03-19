from fastapi import APIRouter, Depends
from fastapi_filter import FilterDepends
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import delete, select
from sqlalchemy.orm import Session
from api_models.oap.propeditclasses import (
    OapPropEditClassesListCreate,
    OapPropEditClassesListFilter,
    OapPropEditClassesListOut,
    OapPropEditClassesListUpdate,
    OapPropEditClassesListWithItemsOut,
)
from api_models.util.model_scheme import get_simple_model_scheme
from models import generate_session
from models.oap import OapPropEditClassesItemDB, OapPropEditClassesListDB
from sqlalchemy.orm import joinedload
from fastapi_pagination import Page
from routes import util
from sqlalchemy.orm import joinedload, selectinload

from sqlalchemy import select, func

router = APIRouter(prefix="/propedit2classeslist")


@router.get("/scheme")
def read_scheme(extensive: bool = False):
    """
    return propedit2classeslist scheme
    """
    scheme =  OapPropEditClassesListOut.model_json_schema() if extensive else get_simple_model_scheme(OapPropEditClassesListOut)
    return scheme

@router.get("/{list_id}/items", response_model=OapPropEditClassesListWithItemsOut)
def read_list_items(
    list_id: int,
    session: Session = Depends(generate_session),
):
    """
    return list items by id
    """
    select_stmt = (
        select(OapPropEditClassesListDB)
        .options(selectinload(OapPropEditClassesListDB.ref_items))
        .filter(OapPropEditClassesListDB.id == list_id)
    )

    print("select_stmt..........")
    print(select_stmt)

    item = session.execute(select_stmt).scalar_one()
    return item


@router.get("/{list_id}", response_model=OapPropEditClassesListOut)
def read_list(
    list_id: int,
    session: Session = Depends(generate_session),
):
    """
    return propedit2classeslist by id
    """
    select_stmt = select(OapPropEditClassesListDB).filter(
        OapPropEditClassesListDB.id == list_id
    )
    item = session.execute(select_stmt).scalar_one()
    return item


@router.get("")
def read_lists(
    session: Session = Depends(generate_session),
    list_filter=FilterDepends(OapPropEditClassesListFilter),
) -> Page[OapPropEditClassesListOut]:
    """
    return all propedit2classeslist
    """
    return paginate(session, list_filter.filter(select(OapPropEditClassesListDB)))


@router.put("")
def update_list(
    list_: OapPropEditClassesListUpdate,
    session: Session = Depends(generate_session),
):
    """
    update propedit2classeslist
    """
    return util.exec_simple_update(OapPropEditClassesListDB, session, list_)


@router.delete("/{list_id}")
def delete_list(
    list_id: int,
    session: Session = Depends(generate_session),
):
    """
    delete propedit2classeslist
    """
    print("propedit2classeslist::delete_list", list_id)
    return util.exec_simple_delete(OapPropEditClassesListDB, session, list_id)


@router.post("")
def create_list(
    list_: OapPropEditClassesListCreate, session: Session = Depends(generate_session)
):
    """
    create list
    """
    return util.exec_simple_insert(OapPropEditClassesListDB, session, list_)
