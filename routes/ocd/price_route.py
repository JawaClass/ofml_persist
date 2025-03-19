from fastapi import APIRouter, Depends
from fastapi_pagination import Page
from sqlalchemy.orm import Session
from models import generate_session
from models.ocd import OcdPriceDB, OcdTextDB
from api_models.ocd.price import (
    OcdPriceCreateWithText,
    OcdPriceCreateWithoutText,
    OcdPriceFilter,
    OcdPriceOut,
    OcdPriceUpdate,
)
from fastapi_filter import FilterDepends, with_prefix
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from services import generic_service

router = APIRouter(prefix="/price")


@router.get("")
def read_price(
    session: Session = Depends(generate_session),
    text_filter=FilterDepends(OcdPriceFilter),
) -> Page[OcdPriceOut]:
    return paginate(session, text_filter.filter(select(OcdPriceDB)))


@router.get("/{price_id}")
def read_price_by_id(price_id: int, session: Session = Depends(generate_session)):
    return session.execute(
        select(OcdPriceDB)
        .options(joinedload(OcdPriceDB.ref_text))
        .filter(OcdPriceDB.id == price_id)
    ).scalar_one()


@router.post("")
def post_price(
    price: OcdPriceCreateWithoutText, session: Session = Depends(generate_session)
):
    price_db = OcdPriceDB(**price.model_dump())
    session.add(price_db)
    session.commit()
    return price_db.id


@router.put("")
def put_price(price: OcdPriceUpdate, session: Session = Depends(generate_session)):
    price_db = session.get(OcdPriceDB, price.id)
    assert price_db

    for name, value in price.model_dump().items():
        setattr(price_db, name, value)

    session.commit()
    return price_db.id
