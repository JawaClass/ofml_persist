from typing import Any
from fastapi import APIRouter, Depends
from fastapi_pagination import Page
from sqlalchemy.orm import Session
from models import generate_session
from models.ocd import OcdPropertyDB, OcdPropertyValueDB
from api_models.ocd.property import (
    OcdPropertyCreate,
    OcdPropertyFilter,
    OcdPropertyItemFilter,
    OcdPropertyItemOut,
    OcdPropertyOut,
    OcdPropertyUpdate,
    OcdPropertyWithTextOut,
)
from fastapi_filter import FilterDepends, with_prefix
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select
from routes import util
from sqlalchemy.orm import joinedload, selectinload
from services import property_service

router = APIRouter(prefix="/property")


@router.get("/item", response_model=Page[OcdPropertyItemOut])
def read_property_item(
    session: Session = Depends(generate_session),
    query_filter=FilterDepends(OcdPropertyItemFilter),
):
    stmt = property_service.stmt_select_property_item
    return paginate(session, query_filter.filter(stmt))


@router.get("/{property_id}/item", response_model=OcdPropertyItemOut)
def read_property_item_by_id(
    property_id: int, session: Session = Depends(generate_session)
):
    stmt = property_service.stmt_select_property_item.where(
        OcdPropertyDB.id == property_id
    )
    return session.execute(stmt).scalar_one()


@router.get("/{property_id}/text", response_model=OcdPropertyWithTextOut)
def read_property_with_text_by_id(
    property_id: int, session: Session = Depends(generate_session)
):
    stmt = property_service.stmt_select_property_with_text.where(
        OcdPropertyDB.id == property_id
    )
    return session.execute(stmt).scalar_one()


@router.get("/text", response_model=Page[OcdPropertyWithTextOut])
def read_property_with_text(
    session: Session = Depends(generate_session),
    query_filter=FilterDepends(OcdPropertyFilter),
):
    stmt = property_service.stmt_select_property_with_text
    return paginate(session, query_filter.filter(stmt))


@router.get("", response_model=Page[OcdPropertyOut])
def read_property(
    session: Session = Depends(generate_session),
    query_filter=FilterDepends(OcdPropertyFilter),
) -> Page[OcdPropertyOut]:
    return paginate(session, query_filter.filter(select(OcdPropertyDB)))


@router.get("/{property_id}", response_model=OcdPropertyOut)
def read_property_by_id(property_id: int, session: Session = Depends(generate_session)):
    return session.query(OcdPropertyDB).get(property_id)


@router.post("")
def post_property(
    property: OcdPropertyCreate, session: Session = Depends(generate_session)
):
    return util.exec_simple_insert(OcdPropertyDB, session, property)


@router.put("")
def put_property(
    property: OcdPropertyUpdate, session: Session = Depends(generate_session)
):
    return util.exec_simple_update(OcdPropertyDB, session, property).id
