from pprint import pprint
from typing import Any
from sqlalchemy import MetaData, create_engine, Engine, select, text
from sqlalchemy.orm import sessionmaker, Session
from models import metadata
from models.base import SqlAlchemyBase, get_orm_class

def get_foreign_keys(table_name: str, metadata: MetaData=metadata):
    """ Get all foreign key constraints referencing table_name """
 
    foreign_keys = {}
    for table in metadata.tables.values():
        for fk in table.foreign_keys:
            if fk.column.table.name == table_name:  # If it references our target table
                if table.name not in foreign_keys:
                    foreign_keys[table.name] = []
                foreign_keys[table.name].append({
                    "child_column": fk.parent.name,
                    "parent_column": fk.column.name
                })

    return foreign_keys

def get_dependent_rows(session: Session, tablename: str, record_id: int):
    """ Get all dependent rows blocking deletion """

    foreign_keys = get_foreign_keys(tablename)
    dependent_rows: dict[str, list[dict[str, Any]]] = {}

    # orm_class = metadata.tables.get(tablename)
    # assert orm_class is not None
     
    for child_table, fks in foreign_keys.items():
        child_orm_class: SqlAlchemyBase = get_orm_class(child_table)# metadata.tables.get(child_table)
        print("child_orm_class::", type(child_orm_class), "child_table=",child_table)

        for fk in fks:
            child_column = fk["child_column"]

            # select_stmt = select(child_orm_class).filter(getattr(child_orm_class, child_column) == record_id)
            # # rows = session.scalars(select_stmt).all()
            # rows = session.execute(select_stmt, execution_options={"render_map": True}).all()

            check_query = text(f"SELECT * FROM {child_table} WHERE {child_column} = :record_id")
            rows = session.execute(check_query, {"record_id": record_id}).mappings().all() #fetchall()
            
            rows = [dict(r) for r in rows]
        
            if rows:
                dependent_rows[child_table] = rows 

    return [{
        "tablename": tablename,
        "records": records,
        "fields": list(records[0].keys()),
        } for tablename, records in dependent_rows.items()]