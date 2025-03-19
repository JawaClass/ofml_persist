from fastapi import APIRouter, Depends
from fastapi_filter import FilterDepends
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import delete, select
from sqlalchemy.orm import Session
from api_models.oap.actionchoice import (
    OapActionChoiceCreate,
    OapActionChoiceFilter,
    OapActionChoiceItemOut,
    OapActionChoiceOut,
    OapActionChoiceUpdate,
)
from api_models.util.model_scheme import get_simple_model_scheme
from models import generate_session
from models.oap import OapActionChoiceDB
from sqlalchemy.orm import joinedload
from fastapi_pagination import Page
from routes import util
from sqlalchemy.orm import joinedload, selectinload

from sqlalchemy import select, func

router = APIRouter(prefix="/actionchoice")


@router.get("/scheme")
def read_scheme(extensive: bool = False):
    """
    return actionchoice scheme
    """
    scheme =  OapActionChoiceOut.model_json_schema() if extensive else get_simple_model_scheme(OapActionChoiceOut)
    return scheme

@router.get("/{actionchoice_id}/item", response_model=OapActionChoiceItemOut)
@router.get("/{actionchoice_id}", response_model=OapActionChoiceItemOut)
def read_actionchoice(
    actionchoice_id: int,
    session: Session = Depends(generate_session),
):
    """
    return actionchoice by id
    """
    select_stmt = select(OapActionChoiceDB).filter(
        OapActionChoiceDB.id == actionchoice_id
    )
    item = session.execute(select_stmt).scalar_one()
    return item


@router.get("")
def read_actionchoices(
    session: Session = Depends(generate_session),
    actionchoice_filter=FilterDepends(OapActionChoiceFilter),
) -> Page[OapActionChoiceOut]:
    """
    return all actionchoices
    """
    return paginate(session, actionchoice_filter.filter(select(OapActionChoiceDB)))


@router.put("")
def update_actionchoice(
    actionchoice: OapActionChoiceUpdate,
    session: Session = Depends(generate_session),
):
    """
    update actionchoice
    """
    return util.exec_simple_update(OapActionChoiceDB, session, actionchoice)


@router.delete("/{actionchoice_id}")
def delete_actionchoice(
    actionchoice_id: int,
    session: Session = Depends(generate_session),
):
    """
    delete actionchoice
    """
    return util.exec_simple_delete(OapActionChoiceDB, session, actionchoice_id)


@router.post("")
def create_actionchoice(
    actionchoice: OapActionChoiceCreate, session: Session = Depends(generate_session)
):
    """
    create actionchoice
    """
    return util.exec_simple_insert(OapActionChoiceDB, session, actionchoice)


# @router.get("")
# def read_actionchoices(
#     session: Session = Depends(generate_session),
#     actionchoice_filter=FilterDepends(OapActionChoiceFilter),
# ) -> Page[OapActionChoiceOut]:
#     """
#     return all actionchoice
#     """
#     return paginate(session, actionchoice_filter.filter(select(OapActionChoiceDB)))

# @router.get("/items")
# def read_actionchoice_items(
#     session: Session = Depends(generate_session),
#     actionchoice_filter=FilterDepends(OapActionChoiceFilter),
# ) -> Page[OapActionChoiceItemOut]:
#     """
#     return all actionchoice_items
#     """

#     select_stmt = select(OapActionChoiceDB).options(
#         selectinload(OapActionChoiceDB.ref_title),
#         selectinload(OapActionChoiceDB.ref_actionlistlist),
#     )

#     return paginate(session, actionchoice_filter.filter(select_stmt))
