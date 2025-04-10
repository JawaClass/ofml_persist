from pprint import pprint
from fastapi import APIRouter, Depends
from fastapi_filter import FilterDepends
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import delete, insert, select
from sqlalchemy.orm import Session
from api_models.oap.interactor import (
    OapInteractorAddActionUpdate,
    OapInteractorCreate,
    OapInteractorFilter,
    OapInteractorOut,
    OapInteractorItemOut,
    OapInteractorUpdate,
)
from api_models.util.model_scheme import get_simple_model_scheme
from models import generate_session
from models.oap import (
    OapActionDB,
    OapInteractorActionAssocDB,
    OapInteractorDB,
    OapPropEdit2DB,
    OapPropEditPropsListDB,
    OapSymbolDisplayDB,
)
from services import article_service
from sqlalchemy.orm import joinedload
from fastapi_pagination import Page
from routes import util
from sqlalchemy.orm import joinedload, selectinload

from sqlalchemy import select, func

router = APIRouter(prefix="/interactor")


@router.get("/scheme")
def read_scheme(extensive: bool = False):
    """
    return interactor scheme
    """
    scheme =  OapInteractorOut.model_json_schema() if extensive else get_simple_model_scheme(OapInteractorOut)
    return scheme

@router.get("")
def read_interactors(
    session: Session = Depends(generate_session),
    interactor_filter=FilterDepends(OapInteractorFilter),
) -> Page[OapInteractorOut]:
    """
    return all interactors
    """
    return paginate(session, interactor_filter.filter(select(OapInteractorDB)))


@router.get("/{interactor_id}", response_model=OapInteractorItemOut)
@router.get("/{interactor_id}/item", response_model=OapInteractorItemOut)
def read_interactor_item(
    interactor_id: int,
    session: Session = Depends(generate_session),
):
    """
    return item by id
    """
    print("read_interactor_item by ID......", interactor_id)
    select_stmt = (
        select(OapInteractorDB)
        .options(
            selectinload(OapInteractorDB.ref_symboldisplays).options(
                selectinload(OapSymbolDisplayDB.ref_direction),
                selectinload(OapSymbolDisplayDB.ref_offset),
                selectinload(OapSymbolDisplayDB.ref_orientation_x),
            ),
            selectinload(OapInteractorDB.actions).options(
                # selectinload(OapActionDB.ref_methodcall),
                # selectinload(OapActionDB.ref_message),
                # selectinload(OapActionDB.ref_actionchoice),
                # selectinload(OapActionDB.ref_createobj),
                # selectinload(OapActionDB.ref_dimchange),
                # selectinload(OapActionDB.ref_extmedia),
                # selectinload(OapActionDB.ref_objects),
                # selectinload(OapActionDB.ref_propchange),
                # selectinload(OapActionDB.ref_propedit),
                # selectinload(OapActionDB.ref_propedit2).options(
                #     selectinload(OapPropEdit2DB.ref_title),
                #     selectinload(OapPropEdit2DB.ref_propeditprops_list).options(
                #         selectinload(OapPropEditPropsListDB.ref_items)
                #     ),
                #     selectinload(OapPropEdit2DB.ref_propeditclasses_list),
                # ),
            ),
        )
        .filter(OapInteractorDB.id == interactor_id)
    )

    item = session.execute(select_stmt).scalar_one()

    return item
 

@router.put("")
def update_interactor(
    interactor: OapInteractorUpdate,
    session: Session = Depends(generate_session),
):
    """
    update interactor
    """
    return util.exec_simple_update(OapInteractorDB, session, interactor)


@router.post("")
def create_interactor(
    interactor: OapInteractorCreate,
    session: Session = Depends(generate_session),
):
    """
    create interactor
    """
    return util.exec_simple_insert(OapInteractorDB, session, interactor)


@router.delete("/{interactor_id}/actions/{action_id}")
def delete_action_by_id(
    interactor_id: int, action_id: int, session: Session = Depends(generate_session)
) -> int:
    """
    delete action relationship by id
    """
    delete_stmt = delete(OapInteractorActionAssocDB).filter(
        OapInteractorActionAssocDB.interactor_id == interactor_id,
        OapInteractorActionAssocDB.action_id == action_id,
    )
    result = session.execute(delete_stmt)
    session.commit()
    return result.rowcount


@router.post("/{interactor_id}/actions/{action_id}")
def add_action_by_id(
    interactor_id: int,
    action_id: int,
    add_action_update: OapInteractorAddActionUpdate,
    session: Session = Depends(generate_session),
) -> int:
    """
    add action relationship by id and position index
    """
    print("add_action_by_id...", interactor_id, "::", add_action_update)

    insert_stmt = insert(OapInteractorActionAssocDB).values(
        interactor_id=interactor_id,
        action_id=action_id,
        position=add_action_update.position_idx,
    )

    result = session.execute(insert_stmt)
    session.commit()
    return result.rowcount


@router.delete("/{interactor_id}")
def delete_interactor(
    interactor_id: int,
    session: Session = Depends(generate_session),
):
    """
    delete interactor
    """
    return util.exec_simple_delete(OapInteractorDB, session, interactor_id)
