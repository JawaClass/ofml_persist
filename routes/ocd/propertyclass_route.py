from fastapi import APIRouter, Depends
from fastapi_pagination import Page
from sqlalchemy.orm import Session
from models import generate_session
from models.ocd import OcdPropertyClassDB, OcdPropertyDB, OcdPropertyValueDB
from api_models.ocd.propertyclass import (
    OcdPropertyclassCreate,
    OcdPropertyclassFilter,
    OcdPropertyclassItemOut,
    OcdPropertyclassOut,
    OcdPropertyclassUpdate,
    OcdPropertyclassWithTextOut,
)
from fastapi_filter import FilterDepends, with_prefix
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select
from routes import util
from sqlalchemy.orm import joinedload, selectinload

router = APIRouter(prefix="/propertyclass")


@router.get("/{propertyclass_id}/item", response_model=OcdPropertyclassItemOut)
def read_propertyclass_item(
    propertyclass_id: int,
    session: Session = Depends(generate_session),
) -> Page[OcdPropertyclassOut]:
    stmt = (
        select(OcdPropertyClassDB)
        .options(
            selectinload(OcdPropertyClassDB.ref_text),
            selectinload(OcdPropertyClassDB.ref_properties).options(
                selectinload(OcdPropertyDB.ref_text),
                selectinload(OcdPropertyDB.ref_property_value).selectinload(
                    OcdPropertyValueDB.ref_text
                ),
            ),
        )
        .where(OcdPropertyClassDB.id == propertyclass_id)
    )
    return session.execute(stmt).scalar_one()


@router.get("/text", response_model=OcdPropertyclassWithTextOut)
def read_propertyclass_with_text(
    session: Session = Depends(generate_session),
    text_filter=FilterDepends(OcdPropertyclassFilter),
) -> Page[OcdPropertyclassOut]:
    stmt = select(OcdPropertyClassDB).options(
        selectinload(OcdPropertyClassDB.ref_text),
    )
    return paginate(session, text_filter.filter(stmt))


@router.get("", response_model=Page[OcdPropertyclassOut])
def read_propertyclass(
    session: Session = Depends(generate_session),
    text_filter=FilterDepends(OcdPropertyclassFilter),
) -> Page[OcdPropertyclassOut]:
    return paginate(session, text_filter.filter(select(OcdPropertyClassDB)))


@router.get("/{propertyclass_id}", response_model=OcdPropertyclassOut)
def read_propertyclass_by_id(
    propertyclass_id: int, session: Session = Depends(generate_session)
):
    return session.query(OcdPropertyClassDB).get(propertyclass_id)


@router.post("")
def post_propertyclass(
    property: OcdPropertyclassCreate, session: Session = Depends(generate_session)
):
    return util.exec_simple_insert(OcdPropertyClassDB, session, property)


@router.put("")
def put_propertyclass(
    property: OcdPropertyclassUpdate, session: Session = Depends(generate_session)
):
    return util.exec_simple_update(OcdPropertyClassDB, session, property).id
