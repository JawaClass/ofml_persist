from fastapi import APIRouter, Depends
from fastapi_filter import FilterDepends
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import delete, select
from sqlalchemy.orm import Session
from api_models.oap.article2type import OapArticle2TypeCreate, OapArticle2TypeFilter, OapArticle2TypeOut, OapArticle2TypeUpdate
from api_models.util.model_scheme import get_simple_model_scheme
from models import generate_session
from models.oap import OapArticle2TypeDB
from sqlalchemy.orm import joinedload
from fastapi_pagination import Page
from routes import util
from sqlalchemy.orm import joinedload, selectinload

from sqlalchemy import select, func

router = APIRouter(prefix="/article2type")


@router.get("/scheme")
def read_scheme(extensive: bool = False):
    """
    return article2type scheme
    """
    scheme =  OapArticle2TypeOut.model_json_schema() if extensive else get_simple_model_scheme(OapArticle2TypeOut)
    return scheme

@router.get("")
def read_article2types(
    session: Session = Depends(generate_session),
    article2type_filter=FilterDepends(OapArticle2TypeFilter),
) -> Page[OapArticle2TypeOut]:
    """
    return all article2types
    """
    return paginate(session, article2type_filter.filter(select(OapArticle2TypeDB)))



@router.post("")
def create_article2type(article2type: OapArticle2TypeCreate, session: Session = Depends(generate_session)):
    """
    create article2type
    """
    return util.exec_simple_insert(OapArticle2TypeDB, session, article2type)


@router.put("")
def create_article2type(article2type: OapArticle2TypeUpdate, session: Session = Depends(generate_session)):
    """
    update article2type
    """
    return util.exec_simple_update(OapArticle2TypeDB, session, article2type)



@router.delete("/{article2type_id}")
def delete_article2type(
    article2type_id: int,
    session: Session = Depends(generate_session),
):
    """
    delete article2type
    """
    return util.exec_simple_delete(OapArticle2TypeDB, session, article2type_id)