from fastapi import APIRouter, Depends
from fastapi_filter import FilterDepends
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import delete, select
from sqlalchemy.orm import Session
from api_models.oap.symboldisplay import (
    OapSymbolDisplayCreate,
    OapSymbolDisplayFilter,
    OapSymbolDisplayItemOut,
    OapSymbolDisplayOut,
    OapSymbolDisplayUpdate,
)
from api_models.util.model_scheme import get_simple_model_scheme
from models import generate_session
from sqlalchemy.orm import joinedload
from fastapi_pagination import Page
from models.oap import OapSymbolDisplayDB
from routes import util
from sqlalchemy.orm import joinedload, selectinload

from sqlalchemy import select, func

router = APIRouter(prefix="/symboldisplay")


@router.get("/scheme")
def read_scheme(extensive: bool = False):
    """
    return symboldisplay scheme
    """
    scheme =  OapSymbolDisplayOut.model_json_schema() if extensive else get_simple_model_scheme(OapSymbolDisplayOut)
    return scheme

@router.get("")
def read_symboldisplays(
    session: Session = Depends(generate_session),
    symboldisplay_filter=FilterDepends(OapSymbolDisplayFilter),
) -> Page[OapSymbolDisplayOut]:
    """
    return all symboldisplay
    """
    return paginate(session, symboldisplay_filter.filter(select(OapSymbolDisplayDB)))


@router.get("/{symboldisplay_id}/item", response_model=OapSymbolDisplayItemOut)
@router.get("/{symboldisplay_id}", response_model=OapSymbolDisplayItemOut)
def read_symboldisplay(
    symboldisplay_id: int,
    session: Session = Depends(generate_session),
):
    """
    return symboldisplay by id
    """
    select_stmt = select(OapSymbolDisplayDB).filter(OapSymbolDisplayDB.id == symboldisplay_id)
    item = session.execute(select_stmt).scalar_one()
    return item

@router.put("", response_model=OapSymbolDisplayItemOut)
def update_symboldisplay(
    symboldisplay: OapSymbolDisplayUpdate,
    session: Session = Depends(generate_session),
):
    """
    update symboldisplay
    """
    updated_symboldisplay = util.exec_simple_update(
        OapSymbolDisplayDB, session, symboldisplay
    )

    select_stmt = (
        select(OapSymbolDisplayDB)
        .options(
            selectinload(OapSymbolDisplayDB.ref_direction),
            selectinload(OapSymbolDisplayDB.ref_offset),
            selectinload(OapSymbolDisplayDB.ref_orientation_x),
        )
        .filter(OapSymbolDisplayDB.id == updated_symboldisplay.id)
    )

    return session.execute(select_stmt).scalar_one()


@router.delete("/{symboldisplay_id}")
def delete_symboldisplay(
    symboldisplay_id: int,
    session: Session = Depends(generate_session),
):
    """
    delete symboldisplay
    """
    return util.exec_simple_delete(OapSymbolDisplayDB, session, symboldisplay_id)


@router.post("")
def create_symboldisplay(
    symboldisplay: OapSymbolDisplayCreate, session: Session = Depends(generate_session)
):
    """
    create symboldisplay
    """
    return util.exec_simple_insert(OapSymbolDisplayDB, session, symboldisplay)
