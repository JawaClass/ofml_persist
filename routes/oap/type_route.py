from fastapi import APIRouter, Depends, HTTPException, Path
from fastapi_filter import FilterDepends
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import delete, select, insert
from sqlalchemy.orm import Session
from api_models.oap.type import (
    OapTypeCreate,
    OapTypeFilter,
    OapTypeItemOut,
    OapTypeOut,
    OapTypeUpdate,
)
from api_models.util.model_scheme import get_simple_model_scheme
from models import generate_session
from models.oap import OapTypeDB, oap_type_interactor_association_table
from fastapi_pagination import Page
from routes import util
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, func

router = APIRouter(prefix="/type")


@router.get("/scheme")
def read_scheme(extensive: bool = False):
    """
    return type scheme
    """
    scheme =  OapTypeOut.model_json_schema() if extensive else get_simple_model_scheme(OapTypeOut)
    return scheme


@router.get("/{type_id:int}/item", response_model=OapTypeItemOut)
@router.get("/{type_id:int}", response_model=OapTypeItemOut)
def read_type(
    type_id: int = Path(..., title="Type ID"),
    session: Session = Depends(generate_session),
):
    """
    return type by id
    """
    select_stmt = select(OapTypeDB).filter(OapTypeDB.id == type_id)
    item = session.execute(select_stmt).scalar_one()
    return item

@router.delete("/{type_id:int}/interactors/{interactor_id:int}")
def delete_interactor_by_id(
    type_id: int, interactor_id: int, session: Session = Depends(generate_session)
) -> int:
    """
    delete interactor relationship by id
    """
    delete_stmt = delete(oap_type_interactor_association_table).filter(
        oap_type_interactor_association_table.c.oap_type_id == type_id,
        oap_type_interactor_association_table.c.oap_interactor_id == interactor_id,
    )
    result = session.execute(delete_stmt)
    session.commit()
    return result.rowcount


@router.post("/{type_id:int}/interactors/{interactor_id:int}")
def add_interactor_by_id(
    type_id: int, interactor_id: int, session: Session = Depends(generate_session)
) -> int:
    """
    add interactor relationship by id
    """
    insert_stmt = insert(oap_type_interactor_association_table).values(
        oap_type_id=type_id,
        oap_interactor_id=interactor_id,
    )
    return util.exec_insert_stmt_plain(insert_stmt, session=session).rowcount 


@router.get("")
def read_types(
    session: Session = Depends(generate_session),
    type_filter=FilterDepends(OapTypeFilter),
) -> Page[OapTypeOut]:
    """
    return all types
    """
    return paginate(session, type_filter.filter(select(OapTypeDB)))


@router.get("/items")
def read_type_items(
    session: Session = Depends(generate_session),
    type_filter=FilterDepends(OapTypeFilter),
) -> Page[OapTypeItemOut]:
    """
    return all type items
    """
    select_stmt = select(OapTypeDB).options(
        selectinload(OapTypeDB.ref_interactor),
        selectinload(OapTypeDB.ref_article2type),
        selectinload(OapTypeDB.ref_metatype2type),
    )
    return paginate(session, type_filter.filter(select_stmt))


@router.put("")
def update_type(
    type: OapTypeUpdate,
    session: Session = Depends(generate_session),
):
    """
    update type
    """
    return util.exec_simple_update(OapTypeDB, session, type)


@router.delete("/{type_id}")
def delete_type(
    type_id: int,
    session: Session = Depends(generate_session),
):
    """
    delete type
    """
    return util.exec_simple_delete(OapTypeDB, session, type_id)


@router.post("")
def create_type(type_: OapTypeCreate, session: Session = Depends(generate_session)):
    """
    create type
    """
    return util.exec_simple_insert(OapTypeDB, session, type_)
