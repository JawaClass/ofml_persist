from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_filter import FilterDepends
from fastapi_pagination.ext.sqlalchemy import paginate
from pydantic import BaseModel
from sqlalchemy import create_engine, delete, select
from sqlalchemy.orm import Session
from api_models.oap.program import (
    OapProgramFilter,
    OapProgramOut,
    OapProgramUpdate,
    OapProgramCreate,
)
from api_models.oap_maker.oap_maker import ExportOapProgram, ImportOapProgram
from models import generate_session, get_engine
from models.oap import OapProgramDB
from sqlalchemy.orm import joinedload
from fastapi_pagination import Page
from ofml_import.oap.import_controller import import_oap
from constants import root_path
from routes import util
from sqlalchemy.orm import joinedload, selectinload
from constants import path_testumgebung
from sqlalchemy import select, func, exists, update
from services.oap import program_service
import traceback

router = APIRouter(prefix="/program")


class OapProgramWithUnresolvedEntriesOut(BaseModel):
    program: OapProgramOut
    unresolved_entries: dict[str, Any] | None = None

@router.post("/import/testumgebung")
def import_oap_from_testumgebung(
    params: ImportOapProgram,
    session: Session = Depends(generate_session),
) -> OapProgramWithUnresolvedEntriesOut:
    """
    import a program from testumgebung
    """
    print("import_oap_from_testumgebung...", params)
    name = params.name
    program_service.assert_program_name_available(name, session)
    
    try:
        result = import_oap(name, session)
    except Exception as e:
        print(f"import {params} failed:", type(e), e)

        exc_traceback = traceback.format_exc()
        print(exc_traceback)
        
        notes = "\n".join(e.__notes__) if "__notes__" in e.__dict__ else exc_traceback
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,  # You can choose the status code you need
            detail=f"""Import failed:\n{notes}""",
        )
    
    imported_program = result.p.program
    imported_program.create_date = str(imported_program.create_date)
    
    p_out = OapProgramOut(
        create_date=imported_program.create_date,
        deleted=imported_program.deleted,
        description=imported_program.description,
        id=imported_program.id,
        import_path=imported_program.import_path,
        name=imported_program.name,
        oap_version=imported_program.oap_version, 
    )
    print("p_out...", type(p_out))
    print(p_out)
    print("result.p.unresolved_entries...", type(result.p.unresolved_entries))
    fmt_dict = {k: [str(_) for _ in v] for k, v  in result.p.unresolved_entries.items()}
    fmt_dict = fmt_dict if len(fmt_dict) else None
    rv = OapProgramWithUnresolvedEntriesOut(program=p_out, unresolved_entries=fmt_dict)
    return rv


@router.post("/export")
def export_oap_program(
    params: ExportOapProgram,
    session: Session = Depends(generate_session),
) -> str:
    from ofml_export.oap.export import export

    program = params.name
    
    return export(program, engine=get_engine()) 


@router.get("/{program_id}", response_model=OapProgramOut)
def read_program(
    program_id: int,
    session: Session = Depends(generate_session),
):
    """
    return program by id
    """
    select_stmt = select(OapProgramDB).filter(OapProgramDB.id == program_id)
    item = session.execute(select_stmt).scalar_one()
    return item


@router.delete("/{program_id}")
def delete_program(
    program_id: int,
    session: Session = Depends(generate_session),
):
    """
    delete program
    """
    item = session.get(OapProgramDB, program_id)
    assert item, f"delete program with id {program_id} doesnt exist"
    assert not item.deleted, f"delete program with id {program_id} was already deleted"
    item.deleted = True
    from time import time

    delete_marker = f"DELETED_{time()}"
    unique_deleted_name = f"{item.name}_{delete_marker}"
    item.name = unique_deleted_name
    session.commit()
    return None


@router.get("")
def read_programs(
    session: Session = Depends(generate_session),
    program_filter=FilterDepends(OapProgramFilter),
) -> Page[OapProgramOut]:
    """
    return all programs
    """
    return paginate(session, program_filter.filter(select(OapProgramDB)))


@router.put("")
def update_program(
    program: OapProgramUpdate,
    session: Session = Depends(generate_session),
):
    """
    update program
    """
    return util.exec_simple_update(OapProgramDB, session, program)


@router.post("")
def create_program(
    program: OapProgramCreate, session: Session = Depends(generate_session)
):
    """
    create propedit
    """
    return util.exec_simple_insert(OapProgramDB, session, program)
