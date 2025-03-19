from fastapi import APIRouter, Depends
from fastapi_filter import FilterDepends
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import delete, select
from sqlalchemy.orm import Session
from api_models.oap.text import OapTextCreate, OapTextFilter, OapTextOut, OapTextUpdate
from api_models.util.model_scheme import get_simple_model_scheme
from models import generate_session
from models.oap import OapTextDB
from sqlalchemy.orm import joinedload
from fastapi_pagination import Page
from routes import util
from sqlalchemy.orm import joinedload, selectinload

from sqlalchemy import select, func

from routes.pagination import LargePage

router = APIRouter(prefix="/text")


@router.get("/scheme")
def read_scheme(extensive: bool = False):
    """
    return text scheme
    """
    scheme =  OapTextOut.model_json_schema() if extensive else get_simple_model_scheme(OapTextOut)
    return scheme

@router.get("/{text_id}", response_model=OapTextOut)
def read_text(
    text_id: int,
    session: Session = Depends(generate_session),
):
    """
    return text by id
    """
    select_stmt = select(OapTextDB).filter(OapTextDB.id == text_id)
    item = session.execute(select_stmt).scalar_one()
    return item


@router.get("")
def read_texts(
    session: Session = Depends(generate_session),
    text_filter=FilterDepends(OapTextFilter),
) -> LargePage[OapTextOut]:
    """
    return all texts
    """
    return paginate(session, text_filter.filter(select(OapTextDB)))


@router.put("")
def update_text(
    text: OapTextUpdate,
    session: Session = Depends(generate_session),
):
    """
    update text
    """
    return util.exec_simple_update(OapTextDB, session, text)


@router.delete("/{text_id}")
def delete_text(
    text_id: int,
    session: Session = Depends(generate_session),
):
    """
    delete text
    """
    return util.exec_simple_delete(OapTextDB, session, text_id)


@router.post("")
def create_text(text: OapTextCreate, session: Session = Depends(generate_session)):
    """
    create text
    """
    return util.exec_simple_insert(OapTextDB, session, text)
