from fastapi import APIRouter, Depends
from fastapi_filter import FilterDepends
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import delete, select
from sqlalchemy.orm import Session
from api_models.oap.numtripel import (
    OapNumTripelCreate,
    OapNumTripelFilter,
    OapNumTripelOut,
    OapNumTripelUpdate,
)
from api_models.util.model_scheme import get_simple_model_scheme
from models import generate_session
from models.oap import OapNumTripelDB
from sqlalchemy.orm import joinedload
from fastapi_pagination import Page
from routes import util
from sqlalchemy.orm import joinedload, selectinload

from sqlalchemy import select, func

from routes.pagination import LargePage

router = APIRouter(prefix="/numtripel")


@router.get("/scheme")
def read_scheme(extensive: bool = False):
    """
    return numtripel scheme
    """
    scheme =  OapNumTripelOut.model_json_schema() if extensive else get_simple_model_scheme(OapNumTripelOut)
    return scheme

@router.get("")
def read_numtripels(
    session: Session = Depends(generate_session),
    numtripel_filter=FilterDepends(OapNumTripelFilter),
) -> LargePage[OapNumTripelOut]:
    """
    return all numtripel
    """
    return paginate(session, numtripel_filter.filter(select(OapNumTripelDB)))


@router.get("/{numtripel_id}", response_model=OapNumTripelOut)
def read_numtripel(
    numtripel_id: int,
    session: Session = Depends(generate_session),
):
    """
    return numTripel by id
    """
    select_stmt = select(OapNumTripelDB).filter(OapNumTripelDB.id == numtripel_id)
    item = session.execute(select_stmt).scalar_one()
    return item

@router.put("")
def update_numtripel(
    numtripel: OapNumTripelUpdate,
    session: Session = Depends(generate_session),
):
    """
    update numTripel
    """
    return util.exec_simple_update(OapNumTripelDB, session, numtripel)


@router.delete("/{numtripel_id}")
def delete_numtripel(
    numtripel_id: int,
    session: Session = Depends(generate_session),
):
    """
    delete numtripel
    """
    return util.exec_simple_delete(OapNumTripelDB, session, numtripel_id)


@router.post("")
def create_numtripel(
    numtripel: OapNumTripelCreate, session: Session = Depends(generate_session)
):
    """
    create numtripel
    """
    print("create_numtripel...", numtripel)
    return util.exec_simple_insert(OapNumTripelDB, session, numtripel)
