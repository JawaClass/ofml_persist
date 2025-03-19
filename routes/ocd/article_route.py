from fastapi import APIRouter, Depends
from fastapi_filter import FilterDepends
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import delete, select
from sqlalchemy.orm import Session
from api_models.ocd.article import (
    OcdArticleFilter,
    OcdArticleOut,
    OcdArticleCreate,
    OcdArticleUpdate,
    OcdArticleWithPriceOut,
    OcdArticleWithTextOut,
    OcdArticleItemFilter,
    OcdArticleItemOut,
)
from api_models.ocd.price import OcdPriceFilter
from api_models.ocd.text import OcdTextCreate, OcdTextUpdate
from models import generate_session
from models.ocd import OcdArticleDB, OcdPriceDB, OcdTextDB
from services import article_service
from sqlalchemy.orm import joinedload
from fastapi_pagination import Page
from routes import util
from sqlalchemy.orm import joinedload, selectinload

from sqlalchemy import select, func

router = APIRouter(prefix="/articles")


@router.get("")
def read_articles(
    session: Session = Depends(generate_session),
    article_filter=FilterDepends(OcdArticleFilter),
) -> Page[OcdArticleOut]:
    """
    return all articles
    """
    return paginate(session, article_filter.filter(select(OcdArticleDB)))


@router.get("/{article_id}", response_model=OcdArticleOut)
def read_article_by_id(article_id: int, session: Session = Depends(generate_session)):
    return session.get_one(OcdArticleDB, article_id)


@router.get("/{article_id}/text", response_model=OcdArticleWithTextOut)
def read_article_with_text_by_id(
    article_id: int, session: Session = Depends(generate_session)
):
    return session.execute(
        select(OcdArticleDB)
        .options(joinedload(OcdArticleDB.ref_short_text))
        .options(joinedload(OcdArticleDB.ref_long_text))
        .filter(OcdArticleDB.id == article_id)
    ).scalar_one()


@router.get("/{article_id}/price", response_model=OcdArticleWithPriceOut)
def read_article_with_price_by_id(
    article_id: int, session: Session = Depends(generate_session)
):
    return (
        session.execute(
            select(OcdArticleDB)
            .options(joinedload(OcdArticleDB.ref_price))
            .filter(OcdArticleDB.id == article_id)
        )
        .unique()
        .scalar_one()
    )


stmt_article_items = select(OcdArticleDB).options(
    selectinload(OcdArticleDB.ref_program),
    selectinload(OcdArticleDB.ref_short_text),
    selectinload(OcdArticleDB.ref_long_text),
    selectinload(OcdArticleDB.ref_propertyclasses),
    selectinload(OcdArticleDB.ref_price_article_only_view),
)


@router.get("/item/", response_model=Page[OcdArticleItemOut])
def read_articleitems(
    session: Session = Depends(generate_session),
    article_filter=FilterDepends(OcdArticleItemFilter),
):
    filtered = article_filter.filter(stmt_article_items)
    return paginate(session, filtered)


@router.get("/{article_id}/item", response_model=OcdArticleItemOut)
def read_articleitem_by_id(
    article_id: int, session: Session = Depends(generate_session)
):
    stmt = stmt_article_items.filter(OcdArticleDB.id == article_id)
    return session.execute(stmt).unique().scalar_one()


@router.post("")
def post_article(
    article: OcdArticleCreate, session: Session = Depends(generate_session)
):
    return util.exec_simple_insert(OcdArticleDB, session, article)


@router.put("/{article_id}/shorttext")
@router.post("/{article_id}/shorttext")
def update_article_shorttext(
    article_id: int,
    text: OcdTextCreate | OcdTextUpdate,
    session: Session = Depends(generate_session),
):
    article = session.get_one(OcdArticleDB, article_id)
    text_assoc_size = session.execute(
        select(func.count(OcdArticleDB.id)).where(
            OcdArticleDB.short_text_id == article.short_text_id
        )
    ).scalar_one()
    text_present = article.ref_short_text
    if text_present is None or text_assoc_size > 1:
        article.ref_short_text = OcdTextDB(**text.model_dump())
    else:
        util.exec_simple_update(OcdTextDB, session, text)

    session.add(article)
    session.commit()
    return article.ref_short_text.id


@router.put("/{article_id}/longtext")
@router.post("/{article_id}/longtext")
def update_article_longtext(
    article_id: int,
    text: OcdTextCreate | OcdTextUpdate,
    session: Session = Depends(generate_session),
):
    article = session.get_one(OcdArticleDB, article_id)
    text_assoc_size = session.execute(
        select(func.count(OcdArticleDB.id)).where(
            OcdArticleDB.long_text_id == article.long_text_id
        )
    ).scalar_one()
    text_present = article.ref_long_text
    print("update_article_longtext", ":: text_present=", text_present)
    if text_present is None or text_assoc_size > 1:
        article.ref_long_text = OcdTextDB(**text.model_dump())
    else:
        util.exec_simple_update(OcdTextDB, session, text)

    session.add(article)
    session.commit()
    return article.ref_long_text.id


@router.delete("/{article_id}/longtext")
def delete_article_longtext(
    article_id: int, session: Session = Depends(generate_session)
):
    article = session.get_one(OcdArticleDB, article_id)
    assert article.long_text_id is not None
    article.long_text_id = None
    session.add(article)
    session.commit()
    return None


@router.delete("/{article_id}/shorttext")
def delete_article_shorttext(
    article_id: int, session: Session = Depends(generate_session)
):
    article = session.get_one(OcdArticleDB, article_id)
    assert article.short_text_id is not None
    article.short_text_id = None
    session.add(article)
    session.commit()
    return None


@router.delete("/{article_id}/price")
def delete_article_price(
    article_id: int,
    session: Session = Depends(generate_session),
    price_filter=FilterDepends(OcdPriceFilter),
):
    select_stmt = price_filter.filter(
        select(OcdPriceDB).where(OcdPriceDB.article_id == article_id)
    )
    select_ids_stmt = select(select_stmt.c.id).select_from(select_stmt)
    delete_stmt = delete(OcdPriceDB).where(OcdPriceDB.id.in_(select_ids_stmt))
    result = session.execute(delete_stmt)
    session.commit()
    return result.rowcount


@router.put("")
def put_article(
    article: OcdArticleUpdate, session: Session = Depends(generate_session)
):
    return util.exec_simple_update(OcdArticleDB, session, article).id


@router.delete("/{article_id}")
def delete_article(
    article_id: int,
    session: Session = Depends(generate_session),
):
    return util.exec_simple_delete(OcdArticleDB, session, article_id)
