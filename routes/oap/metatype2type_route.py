from fastapi import APIRouter, Depends
from fastapi_filter import FilterDepends
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import delete, select
from sqlalchemy.orm import Session
from api_models.oap.metatype2type import OapMetaType2TypeFilter, OapMetaType2TypeItemOut, OapMetaType2TypeOut, OapMetaType2TypeCreate, OapMetaType2TypeUpdate
from api_models.util.model_scheme import get_simple_model_scheme
from models import generate_session
from models.oap import OapArticle2TypeDB, OapMetaType2TypeDB, OapTypeDB
from sqlalchemy.orm import joinedload
from fastapi_pagination import Page
from routes import util
from sqlalchemy.orm import joinedload, selectinload

from sqlalchemy import select, func

router = APIRouter(prefix="/metatype2type")

@router.get("/scheme")
def read_scheme(extensive: bool = False):
    """
    return metatype2type scheme
    """
    scheme =  OapMetaType2TypeOut.model_json_schema() if extensive else get_simple_model_scheme(OapMetaType2TypeOut)
    return scheme


@router.get("/{metatype2type_id}", response_model=OapMetaType2TypeOut)
def read_metatype2type(
    metatype2type_id: int,
    session: Session = Depends(generate_session),
):
    """
    return metatype2type by id
    """
    select_stmt = select(OapMetaType2TypeDB).filter(OapMetaType2TypeDB.id == metatype2type_id)
    item = session.execute(select_stmt).scalar_one()
    return item

@router.get("")
def read_metatype2types(
    session: Session = Depends(generate_session),
    metatype2type_filter=FilterDepends(OapMetaType2TypeFilter),
) -> Page[OapMetaType2TypeOut]:
    """
    return all metatype2types
    """
    select_stmt = select(OapMetaType2TypeDB)
    return paginate(session, metatype2type_filter.filter(select_stmt))

@router.get("/items")
def read_metatype2type_items(
    session: Session = Depends(generate_session),
    metatype2type_filter=FilterDepends(OapMetaType2TypeFilter),
) -> Page[OapMetaType2TypeItemOut]:
    """
    return all metatype2type items
    """
    select_stmt = select(OapMetaType2TypeDB).options(
        selectinload(OapMetaType2TypeDB.ref_type).selectinload(
            OapTypeDB.ref_interactor
        ),
    )
    return paginate(session, metatype2type_filter.filter(select_stmt))



@router.post("")
def create_metatype2type(metatype2type: OapMetaType2TypeCreate, session: Session = Depends(generate_session)):
    """
    create metatype2type
    """
    return util.exec_simple_insert(OapMetaType2TypeDB, session, metatype2type)


@router.put("")
def update_metatype2type(metatype2type: OapMetaType2TypeUpdate, session: Session = Depends(generate_session)):
    """
    update metatype2type
    """
    return util.exec_simple_update(OapMetaType2TypeDB, session, metatype2type)

@router.delete("/{metatype2type_id}")
def delete_metatype2type(
    metatype2type_id: int,
    session: Session = Depends(generate_session),
):
    """
    delete metatype2type
    """
    return util.exec_simple_delete(OapMetaType2TypeDB, session, metatype2type_id)