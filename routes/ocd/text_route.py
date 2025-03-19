from fastapi import APIRouter, Depends
from fastapi_pagination import Page
from sqlalchemy.orm import Session
from models import generate_session
from models.ocd import OcdTextDB
from api_models.ocd.text import OcdTextCreate, OcdTextUpdate, OcdTextFilter, OcdTextOut
from fastapi_filter import FilterDepends, with_prefix
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select
from routes import util

router = APIRouter(prefix="/text")


@router.get("")
def read_text(
    session: Session = Depends(generate_session),
    text_filter=FilterDepends(OcdTextFilter),
) -> Page[OcdTextOut]:
    return paginate(session, text_filter.filter(select(OcdTextDB)))


@router.get("/{text_id}")
def read_text_by_id(text_id: int, session: Session = Depends(generate_session)):
    return session.query(OcdTextDB).get(text_id)


@router.post("")
def post_text(text: OcdTextCreate, session: Session = Depends(generate_session)):
    return util.exec_simple_insert(OcdTextDB, session, text)


@router.put("")
def put_text(text: OcdTextUpdate, session: Session = Depends(generate_session)):
    return util.exec_simple_update(OcdTextDB, session, text).id


@router.delete("/{text_id}")
def delete_text(
    text_id: int,
    session: Session = Depends(generate_session),
):
    return util.exec_simple_delete(OcdTextDB, session, text_id)
