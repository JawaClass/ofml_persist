from pprint import pprint
from typing import Any
from fastapi import APIRouter, Depends
from fastapi_pagination import Page
from sqlalchemy.orm import Session
from api_models.oap.program import OapProgramOut
from models import generate_session
from models.oap import OapProgramDB
from models.ocd import OcdArtbaseDB
from services import article_service
from api_models.ocd.artbase import OcdArtbaseCreate, OcdArtbaseFilter, OcdArtbaseOut
from fastapi_filter import FilterDepends, with_prefix
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select
import ofml_api.repository as ofml

router = APIRouter(prefix="/profiles")


def make_item(db_program: OapProgramOut | None, registry: dict | None, oap_path: str):
    return {
        "db_program": db_program,
        "registry": registry,
        "oap_path": oap_path,
    }


@router.get("/programs", response_model=list[dict[str, Any]])
def read_profile_programs(
    session: Session = Depends(generate_session),
):
    """
    return all programs from plaintext profiles
    """
    repo = ofml.Repository("/mnt/knps_testumgebung/Testumgebung/EasternGraphics", "kn")
    repo.read_profiles()
    programs = [repo.load_program(_) for _ in repo.program_names()]
    programs = [
        _
        for _ in programs
        if isinstance(_, ofml.Program) and _.contains_ofml_part("oap")
    ]
    # select all programs in db
    db_programs = session.scalars(
        select(OapProgramDB).filter(OapProgramDB.deleted == False)
    ).all()
    # simply access to pydantic model
    name2db_program = {
        db_p.name: OapProgramOut.model_validate(db_p) for db_p in db_programs
    }

    db_only_programs = [
        p for p in db_programs if p.name not in set([_.name for _ in programs])
    ]
    # return pair of palintext registry and db program (if exists otherwise None)
    return [
        make_item(
            name2db_program.get(_.registry.config.get("program")),
            _.registry.config,
            "TODO...",
        )
        for _ in programs
    ] + [
        make_item(
            name2db_program[p.name],
            None,
            "TODO...",
        )
        for p in db_only_programs
    ]
