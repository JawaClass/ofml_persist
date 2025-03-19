from fastapi import APIRouter, Depends
from fastapi_pagination import Page
from sqlalchemy.orm import Session
from models import generate_session
from models.ocd import OcdArtbaseDB
from services import article_service
from api_models.ocd.artbase import OcdArtbaseCreate, OcdArtbaseFilter, OcdArtbaseOut
from fastapi_filter import FilterDepends, with_prefix
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import delete, select
from routes import util

router = APIRouter(prefix="/artbase")


@router.get("")
def read_artbase(
    session: Session = Depends(generate_session),
    artbase_filter=FilterDepends(OcdArtbaseFilter),
) -> Page[OcdArtbaseOut]:
    return paginate(session, artbase_filter.filter(select(OcdArtbaseDB)))


@router.get("/{artbase_id}")
def read_artbase_by_id(artbase_id: int, session: Session = Depends(generate_session)):
    return session.query(OcdArtbaseDB).get(artbase_id)


@router.post("")
def post_artbase(
    artbase: OcdArtbaseCreate, session: Session = Depends(generate_session)
):
    print("post_article....")
    print(artbase)
    return util.exec_simple_insert(OcdArtbaseDB, session, artbase)


@router.delete("/{artbase_id}")
def delete_artbase(
    artbase_id: int,
    session: Session = Depends(generate_session),
):
    return util.exec_simple_delete(OcdArtbaseDB, session, artbase_id)


@router.delete("/{pclass}/{prop}/{pvalue}")
def delete_artbase_by_pclass_prop_pvalue(
    pclass: str,
    prop: str,
    pvalue: str | int | float,
    session: Session = Depends(generate_session),
):
    print("delete_artbase_by_pclass_prop_pvalue", pclass, prop, pvalue, type(pvalue))
    session.execute(
        delete(OcdArtbaseDB).where(
            OcdArtbaseDB.class_name == pclass,
            OcdArtbaseDB.prop_name == prop,
            OcdArtbaseDB.prop_value == pvalue,
        )
    )
    session.commit()
