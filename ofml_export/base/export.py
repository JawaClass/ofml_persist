from typing import TypeVar
from models import engine
import pandas as pd
from sqlalchemy.orm import Session, DeclarativeBase
from sqlalchemy import Engine
from abc import ABC, abstractmethod

T = TypeVar("T", bound="ExportBase")


class ExportBase(ABC):

    def __init__(self, program_name: str, engine) -> None:
        self.session = Session(engine)
        self.engine = engine
        self.program_name = program_name
        self.tables: dict[str, pd.DataFrame] = {}

    def read_sql(self, statement) -> pd.DataFrame:
        return pd.read_sql(
            statement,
            self.engine,
        )

    def extract_table_by_ids(
        self, table: DeclarativeBase, id_attr: str, ids: list[int]
    ):
        return self.read_sql(
            self.session.query(table).filter(getattr(table, id_attr).in_(ids)).statement
        )

    @abstractmethod
    def extract(self: T) -> T:
        pass

    @abstractmethod
    def format(self: T) -> T:
        pass

    @abstractmethod
    def export(self):
        pass
