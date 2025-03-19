from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination import Page
from sqlalchemy.orm import Session, selectinload
from models import generate_session
from models.ocd import OcdProgramDB
from api_models.ocd.program import (
    ArticleProgram,
    OcdProgramCreate,
    OcdProgramCreateFromArticles,
    OcdProgramUpdate,
    OcdProgramFilter,
    OcdProgramOut,
    OcdProgramWithCreatorOut,
)
from fastapi_filter import FilterDepends, with_prefix
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select
from routes import util
from ofml_import.ocd.merge_db_articles_from_program_to_program import ofml2dbscheme
from services import program_service

router = APIRouter(prefix="/programs")


@router.get("")
def read_program(
    session: Session = Depends(generate_session),
    program_filter=FilterDepends(OcdProgramFilter),
) -> Page[OcdProgramOut]:
    return paginate(session, program_filter.filter(select(OcdProgramDB)))


@router.get("/item/creators/")
def read_programs_with_creators(
    session: Session = Depends(generate_session),
    program_filter=FilterDepends(OcdProgramFilter),
) -> Page[OcdProgramWithCreatorOut]:
    return paginate(
        session,
        program_filter.filter(
            select(OcdProgramDB).options(selectinload(OcdProgramDB.ref_creator))
        ),
    )


@router.get("/{program_id}")
def read_program_by_id(program_id: int, session: Session = Depends(generate_session)):
    return session.query(OcdProgramDB).get(program_id)


@router.post("")
def post_program(
    program: OcdProgramCreate, session: Session = Depends(generate_session)
):
    return util.exec_simple_insert(OcdProgramDB, session, program)


@router.post("/from_articles")
def post_program_from_articles(
    program: OcdProgramCreateFromArticles, session: Session = Depends(generate_session)
):
    print("post_program/from_articles...")
    existing_program = program_service.get_program_by_name(session, program.name)
    if existing_program:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Program with name {program.name} already exists. Use PUT to add articles to existing program.",
        )
    merge_program = OcdProgramDB(
        name=program.name,
        description=program.description,
        import_path=program.import_path,
    )
    ofml2dbscheme(
        session=session,
        merge_program=merge_program,
        articles=program.article_program_list,
    )
    return merge_program.id


@router.put("{program_id}/from_articles")
def add_articles_to_program(
    program_id: int,
    articles: list[ArticleProgram],
    session: Session = Depends(generate_session),
):
    merge_program = program_service.get_program_by_id(session, program_id)
    if not merge_program:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Program with id {program_id} not found.",
        )
    ofml2dbscheme(session=session, merge_program=merge_program, articles=articles)
    return merge_program.id


@router.put("")
def put_program(text: OcdProgramUpdate, session: Session = Depends(generate_session)):
    return util.exec_simple_update(OcdProgramDB, session, text).id


@router.delete("/{program_id}")
def delete_program(
    program_id: int,
    session: Session = Depends(generate_session),
):
    return util.exec_simple_delete(OcdProgramDB, session, program_id)
