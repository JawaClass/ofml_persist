from fastapi_pagination import paginate
from sqlalchemy import select
from sqlalchemy.orm import Session

from fastapi_filter.contrib.sqlalchemy import Filter
from typing import TypeVar, Generic  

T = TypeVar('T')

def get_by_id(ormCls: T, session: Session, row_id: int) -> T | None:
    return session.query(ormCls).get(row_id)


def get_list(ormCls: T, session: Session, row_id: int, query_filter: Filter) -> list[T]:
    return paginate(session, query_filter.filter(select(ormCls)))
 