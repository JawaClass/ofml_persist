from pprint import pprint
from typing import Any, Callable
import ofml_api.repository as ofml
import pandas as pd
from sqlalchemy import select
from models import generate_session, generate_session_ctx
from models.oap import OapProgramDB
from ofml_import import util
from ofml_import.oap.import_program_plaintext_to_db import InsertOap, ofml2dbscheme

from sqlalchemy.orm import Session
from ofml_api.repository import OFMLPart


class OapImportController:

    def extract_from(
        self,
        table_df: pd.DataFrame,
        extract_method: Callable[..., Any],
        param_names: list[str],
    ):
        for row in table_df.itertuples():
            extract_method(*[getattr(row, _) for _ in param_names])

    def add_obj_to_session(self, orm_obj, commit: bool=False):
        if orm_obj is None:
            return
        if isinstance(orm_obj, list):
            for ch in orm_obj:
                self.add_obj_to_session(ch)
        else:
            self.session.add(orm_obj)
            if commit:
                from sqlalchemy.exc import IntegrityError
                try:
                    self.session.commit()
                except IntegrityError as e:
                    print("IntegrityError...", orm_obj)
                    print(e)
                    tablename = orm_obj.__class__.__tablename__
                    self.p.add_unresolved_entry(tablename, orm_obj)
                    self.session.rollback()
                    # input("...")

    def __init__(
        self,
        oap: OFMLPart,
        session: Session,
        program_name: str,
        description: str | None = None, 
    ) -> None:
        self.session = session
        self.p = InsertOap(oap, session, program_name, description)

        # traverse starting from these parent tables to its child references
        # and collect all rows on the way
        extract_definition = [
            [
                self.p.oap_metatype2type.df,
                self.p.extract_metatype2type,
                ("manufacturer", "series", "metatype_id"),
            ],
            [
                self.p.oap_article2type.df,
                self.p.extract_article2type,
                ("manufacturer_id", "series_id", "article_id"),
            ],
            [
                self.p.oap_action.df,
                self.p.extract_action,
                ("action",),
            ],
        ]

        for t, m, p in extract_definition:
            self.extract_from(t, m, p)

        m = self.p.identy_map_by_key
        orm_objects = [
            orm_obj
            for table_name in m
            for (orm_key, orm_obj) in m[table_name].items()
            if orm_obj is not None
        ]
 
        for o in orm_objects:
            self.add_obj_to_session(o, commit=True)

        # self.session.commit()

        # for table_name, orm_objects in m.items():
        #     print("table_name", table_name, "size:", len(orm_objects))
        #     for k, obj in orm_objects.items():
        #         print("commit...")
        #         print(k, "::", obj)
        #         self.session.add(obj)
        #         self.session.commit()

        # self.p.copy_images()


def import_oap(program_name: str, session: Session):
    repo = ofml.Repository("/mnt/knps_testumgebung/Testumgebung/EasternGraphics", "kn")
    repo.read_profiles()

    existing = session.scalar(
        select(OapProgramDB).where(OapProgramDB.name == program_name)
    )
    assert existing is None, f"Program with name {program_name} does already exist!"

    p = repo.load_program(program_name)
    oap = p.load_ofml_part("oap")
    # oap.read_all_tables()

    for name in oap.filenames_from_tables_definitions:
        print("read_table...", name)
        oap.read_table(name, encoding=None)
    # pprint(oap.tables)
    # input(",,,")
    from time import time

    util.fmt_tables_na2none(oap)
    import_ctrl = OapImportController(oap, session, p.name)
    # return import_ctrl.p.program
    return import_ctrl


if __name__ == "__main__":
    with generate_session_ctx() as session:
        import_oap("workplace", session)
