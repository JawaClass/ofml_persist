from sqlalchemy import exists, select
from sqlalchemy.orm import Session

from models.ocd import OcdProgramDB


def get_all_programs(session: Session):
    return session.execute(select(OcdProgramDB)).scalars().all()


def get_program_by_name(session: Session, name: str):
    return session.execute(
        select(OcdProgramDB).where(OcdProgramDB.name == name)
    ).scalar()


def get_program_by_id(session: Session, program_id: str):
    return session.execute(
        select(OcdProgramDB).where(OcdProgramDB.id == program_id)
    ).scalar()
