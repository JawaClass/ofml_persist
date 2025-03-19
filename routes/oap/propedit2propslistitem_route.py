from fastapi import APIRouter, Depends
from fastapi_filter import FilterDepends
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import delete, select
from sqlalchemy.orm import Session
from api_models.oap.propeditprops import (
    OapPropEditPropsItemOut,
    OapPropEditPropsItemUpdate,
    OapPropEditPropsItemCreate,
    OapPropEditPropsItemFilter,
)
from api_models.util.model_scheme import get_simple_model_scheme
from models import generate_session
from models.oap import OapPropEditPropsItemDB
from sqlalchemy.orm import joinedload
from fastapi_pagination import Page
from routes import util
from sqlalchemy.orm import joinedload, selectinload

from sqlalchemy import select, func

router = APIRouter(prefix="/propedit2propslistitem")


@router.get("/scheme")
def read_scheme(extensive: bool = False):
    """
    return propedit2propslistitem scheme
    """
    scheme =  OapPropEditPropsItemOut.model_json_schema() if extensive else get_simple_model_scheme(OapPropEditPropsItemOut)
    return scheme


@router.get("/{item_id}", response_model=OapPropEditPropsItemOut)
def read_item(
    item_id: int,
    session: Session = Depends(generate_session),
):
    """
    return propedit list items
    """
    select_stmt = select(OapPropEditPropsItemDB).filter(
        OapPropEditPropsItemDB.id == item_id
    )
    item = session.execute(select_stmt).scalar_one()
    return item


@router.get("")
def read_items(
    session: Session = Depends(generate_session),
    item_filter=FilterDepends(OapPropEditPropsItemFilter),
) -> Page[OapPropEditPropsItemOut]:
    """
    return all propedit2propslist
    """
    return paginate(session, item_filter.filter(select(OapPropEditPropsItemDB)))


@router.put("")
def update_item(
    item: OapPropEditPropsItemUpdate,
    session: Session = Depends(generate_session),
):
    """
    update list item
    """
    return util.exec_simple_update(OapPropEditPropsItemDB, session, item)


@router.delete("/{item_id}")
def delete_item(
    item_id: int,
    session: Session = Depends(generate_session),
):
    """
    delete list item
    """
    return util.exec_simple_delete(OapPropEditPropsItemDB, session, item_id)


@router.post("")
def create_item(
    item: OapPropEditPropsItemCreate, session: Session = Depends(generate_session)
):
    """
    create list item
    """
    return util.exec_simple_insert(OapPropEditPropsItemDB, session, item)
