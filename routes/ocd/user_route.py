from fastapi import APIRouter, Depends
from fastapi_pagination import Page
from sqlalchemy.orm import Session
from models import generate_session
from models.ocd import OcdProgramUserAssocDB, OcdUserDB, ProgramPermission, UserRole
from api_models.ocd.user import (
    OcdUserCreate,
    OcdUserUpdate,
    OcdUserFilter,
    OcdUserOut,
)
from fastapi_filter import FilterDepends, with_prefix
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select, delete
from routes import util
from sqlalchemy.orm import joinedload, selectinload
from services import auth_service, user_service

router = APIRouter(prefix="/users")


@router.get("")
def read_user(
    session: Session = Depends(generate_session),
    program_filter=FilterDepends(OcdUserFilter),
) -> Page[OcdUserOut]:
    return paginate(session, program_filter.filter(select(OcdUserDB)))


@router.get("/{user_id}")
def read_user_by_id(user_id: int, session: Session = Depends(generate_session)):
    return session.query(OcdUserDB).get(user_id)


@router.get("/email/{email}", response_model=OcdUserOut)
def read_user_by_email(email: str, session: Session = Depends(generate_session)):
    return user_service.get_user_by_email(session, email)


@router.get("/{user_id}/programs")
def read_user_with_programs_by_id(
    user_id: int, session: Session = Depends(generate_session)
):
    stmt = (
        select(OcdUserDB)
        .options(
            selectinload(OcdUserDB.ref_programs),
        )
        .where(OcdUserDB.id == user_id)
    )
    return session.execute(stmt).scalar_one()


@router.post("")
def post_user(user: OcdUserCreate, session: Session = Depends(generate_session)):
    return user_service.create_user(session, user.email, user.password)


@router.put("")
def put_user(user: OcdUserUpdate, session: Session = Depends(generate_session)):
    return util.exec_simple_update(OcdUserDB, session, user).id


@router.post("/{user_id}/programs")
def add_program_to_user(
    user_id: int,
    program_id: int,
    permission: ProgramPermission,
    session: Session = Depends(generate_session),
):
    # Logic to associate the program with the user
    association = OcdProgramUserAssocDB(
        user_id=user_id, program_id=program_id, permission=permission
    )
    session.add(association)
    session.commit()
    return user_id


@router.delete("/{user_id}/programs/{program_id}")
def remove_program_from_user(
    user_id: int,
    program_id: int,
    session: Session = Depends(generate_session),
):
    # Logic to remove the association
    association = (
        session.query(OcdProgramUserAssocDB)
        .filter(
            OcdProgramUserAssocDB.user_id == user_id,
            OcdProgramUserAssocDB.program_id == program_id,
        )
        .one_or_none()
    )

    if association is None:
        return {"error": "Association not found."}, 404

    session.delete(association)
    session.commit()
    return user_id


@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    session: Session = Depends(generate_session),
):
    return util.exec_simple_delete(OcdUserDB, session, user_id)
