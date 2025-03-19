from fastapi import APIRouter, Depends
from fastapi_pagination import Page
from sqlalchemy.orm import Session
from models import generate_session
from models.ocd import OcdPropertyValueDB
from api_models.ocd.propertyvalue import (
    OcdPropertyvalueCreate,
    OcdPropertyvalueFilter,
    OcdPropertyvalueOut,
    OcdPropertyvalueUpdate,
    OcdPropertyvalueWithTextOut,
)
from fastapi_filter import FilterDepends, with_prefix
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select
from routes import util
from services import propertyvalue_service

router = APIRouter(prefix="/propertyvalue")


@router.get("/{propertyvalue_id}", response_model=OcdPropertyvalueWithTextOut)
def read_propertyvalue_with_text_by_id(
    propertyvalue_id: int, session: Session = Depends(generate_session)
):
    stmt = propertyvalue_service.stmt_select_propertyvalue_with_text.where(
        OcdPropertyValueDB.id == propertyvalue_id
    )
    return session.execute(stmt).scalar_one()


@router.get("", response_model=Page[OcdPropertyvalueOut])
def read_propertyvalue(
    session: Session = Depends(generate_session),
    text_filter=FilterDepends(OcdPropertyvalueFilter),
) -> Page[OcdPropertyvalueOut]:
    return paginate(session, text_filter.filter(select(OcdPropertyValueDB)))


@router.get("/{property_id}", response_model=OcdPropertyvalueOut)
def read_propertyvalue_by_id(
    property_id: int, session: Session = Depends(generate_session)
):
    return session.query(OcdPropertyValueDB).get(property_id)


@router.post("")
def post_propertyvalue(
    property: OcdPropertyvalueCreate, session: Session = Depends(generate_session)
):
    return util.exec_simple_insert(OcdPropertyValueDB, session, property)


@router.put("")
def put_propertyvalue(
    property: OcdPropertyvalueUpdate, session: Session = Depends(generate_session)
):
    return util.exec_simple_update(OcdPropertyValueDB, session, property).id
