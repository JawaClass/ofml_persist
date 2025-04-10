from contextlib import contextmanager
from sqlalchemy import MetaData, create_engine, text

from models.base import SqlAlchemyBase
from sqlalchemy.orm import sessionmaker, Session

from models.oap import *

# from models.ocd import *

from typing import Generator

# engine = create_engine("sqlite+pysqlite:///:memory:", echo=False)
from config import db_config

engine = create_engine(
    f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['db']}",

    # "sqlite+pysqlite:///ofml_sqlite.db",

    echo=0,
    # connect_args={"check_same_thread": False},
)
# input(". drop all")
# SqlAlchemyBase.metadata.drop_all(engine)
SqlAlchemyBase.metadata.create_all(engine)
# print(SqlAlchemyBase.metadata.tables)
# input("create all")


metadata = MetaData()
metadata.reflect(bind=engine)

_new_session = sessionmaker(
    bind=engine, class_=Session, autocommit=False, autoflush=False
)


def get_engine():
    return engine


@contextmanager
def generate_session_ctx():
    return generate_session()


def generate_session() -> Generator[Session, None, None]:
    """
    Dependency function to yield an async SQLAlchemy ORM session.

    Yields:
        AsyncSession: An instance of an async SQLAlchemy ORM session.
    """
    with _new_session() as session:
        # session.execute(
        #     text("PRAGMA foreign_keys = 1")
        # )  # for sqlite to enforce foreign keys
        yield session
