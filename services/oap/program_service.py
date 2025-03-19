from fastapi import HTTPException
from sqlalchemy import exists, select
from models.oap import OapProgramDB
from sqlalchemy.orm import Session
from fastapi import HTTPException, status


def assert_program_name_available(name: str, session: Session):
    stmt = select(exists().where(OapProgramDB.name == name))
    print("stmt...", type(stmt))
    print(stmt)
    program_exists = session.scalar(stmt)

    if program_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,  # You can choose the status code you need
            detail=f"Cannot import {name} because it already exists",
        )
