from fastapi import APIRouter, Depends
from fastapi_filter import FilterDepends
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import delete, select
from sqlalchemy.orm import Session
from api_models.oap.methodcall import (
    OapMethodCallCreate,
    OapMethodCallFilter,
    OapMethodCallOut,
    OapMethodCallUpdate,
)
from api_models.util.model_scheme import get_simple_model_scheme
from models import generate_session
from models.oap import OapMethodCallDB
from sqlalchemy.orm import joinedload
from fastapi_pagination import Page
from routes import util
from sqlalchemy.orm import joinedload, selectinload

from sqlalchemy import select, func

from routes.pagination import LargePage

router = APIRouter(prefix="/methodcall")

@router.get("/scheme")
def read_scheme(extensive: bool = False):
    """
    return methodcall scheme
    """
    scheme =  OapMethodCallOut.model_json_schema() if extensive else get_simple_model_scheme(OapMethodCallOut)
    return scheme
 

@router.get("/{methodcall_id}", response_model=OapMethodCallOut)
def read_methodcall(
    methodcall_id: int,
    session: Session = Depends(generate_session),
):
    """
    return methodcall by id
    """
    select_stmt = select(OapMethodCallDB).filter(OapMethodCallDB.id == methodcall_id)
    item = session.execute(select_stmt).scalar_one()
    return item


@router.get("")
def read_methodcalls(
    session: Session = Depends(generate_session),
    type_filter=FilterDepends(OapMethodCallFilter),
) -> LargePage[OapMethodCallOut]:
    """
    return all methodcalls
    """
    return paginate(session, type_filter.filter(select(OapMethodCallDB)))


@router.put("")
def update_methodcall(
    methodcall: OapMethodCallUpdate,
    session: Session = Depends(generate_session),
):
    """
    update methodcall
    """
    return util.exec_simple_update(OapMethodCallDB, session, methodcall)


@router.delete("/{methodcall_id}")
def delete_methodcall(
    methodcall_id: int,
    session: Session = Depends(generate_session),
):
    """
    delete methodcall
    """
    return util.exec_simple_delete(OapMethodCallDB, session, methodcall_id)


@router.post("")
def create_methodcall(
    methodcall: OapMethodCallCreate, session: Session = Depends(generate_session)
):
    """
    create methodcall
    """
    return util.exec_simple_insert(OapMethodCallDB, session, methodcall)
