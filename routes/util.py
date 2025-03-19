from fastapi import HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import TypeVar
from sqlalchemy.orm import Session
from sqlalchemy import Insert, delete
from sqlalchemy.exc import IntegrityError, DatabaseError
from functools import wraps

from models.ref_integrity_del_links import get_dependent_rows, get_foreign_keys

from sqlalchemy.orm import DeclarativeBase

T = TypeVar("T", bound=DeclarativeBase) # DeclarativeBase


def catch_database_errors(f):
    @wraps(f)
    def execute_f(*args, session: Session, **kwargs):
        try:
            return f(session=session, *args, **kwargs)
        except DatabaseError as e:
            import traceback
            print(traceback.format_exc())
            session.rollback()  # Rollback to avoid partial transactions
            err_detail = ", ".join(e.detail)
            
            raise HTTPException(
                status_code=400,
                detail=f"""Datenbank lehnt diese Aktion ab:
                Details: {err_detail}
                Fehler: {e.orig}
                Stmt: {e.statement}
                Params: {e.params}""",
            )

    return execute_f


@catch_database_errors
def exec_insert_stmt_plain(insert_stmt: Insert, *, session: Session):
    result = session.execute(insert_stmt)
    session.commit()
    return result


def exec_simple_delete(ormCls: T, session: Session, id: int) -> None:
    return _exec_simple_delete(ormCls=ormCls, session=session, id=id)


@catch_database_errors
def _exec_simple_delete(*, ormCls: T, session: Session, id: int) -> None:
    try:
        session.execute(delete(ormCls).where(ormCls.id == id))
        session.commit()
    except IntegrityError as e:  # IntegrityError:
        print("_exec_simple_delete error...", e)
        session.rollback()  # Rollback to avoid partial transactions

        dependent_rows = get_dependent_rows(session, ormCls.__tablename__, id)
        
        if dependent_rows:
            return JSONResponse(
            status_code=400,
            content={
                "error": "Integrity Error",
                "message": f"Cannot delete record {ormCls.__qualname__} with id {id} due to foreign key constraint.",
                "dependent_records": dependent_rows,
            },
            )

        raise HTTPException(
            status_code=400,
            detail=f"Cannot delete item {ormCls.__qualname__} with id {id} because it is referenced by other records.",
        )
    return None

 
def exec_simple_insert(ormCls: T, session: Session, obj: BaseModel) -> T:
    return _exec_simple_insert(ormCls=ormCls, session=session, obj=obj)


@catch_database_errors
def _exec_simple_insert(*, ormCls: T, session: Session, obj: BaseModel) -> T:
    obj_db = ormCls(**obj.model_dump())
    session.add(obj_db)
    session.commit()
    session.refresh(obj_db)
    return obj_db


def exec_simple_update(ormCls: T, session: Session, obj: BaseModel) -> T:
    return _exec_simple_update(ormCls=ormCls, session=session, obj=obj)


@catch_database_errors
def _exec_simple_update(*, ormCls: T, obj: BaseModel, session: Session) -> T:
    obj_db = session.get_one(ormCls, obj.id)

    for name, value in obj.model_dump().items():
        setattr(obj_db, name, value)

    session.commit()
    session.refresh(obj_db)
    return obj_db