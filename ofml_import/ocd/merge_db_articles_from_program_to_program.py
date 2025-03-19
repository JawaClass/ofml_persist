from collections import defaultdict
import functools
from typing import DefaultDict
import pandas as pd
from pprint import pprint
import itertools
from sqlalchemy import and_, select, func
from api_models.ocd.program import ArticleProgram
from models import generate_session
from models.ocd import (
    OcdArticlePropertyclassAssocDB,
    OcdGlobalPackagingDB,
    OcdProgramDB,
    OcdPropertyDB,
    OcdPropertyValueDB,
    OcdRelationObjRelationAssocDB,
    TextType,
    OcdArtbaseDB,
    OcdArticleDB,
    OcdTextDB,
    OcdPriceDB,
    OcdRelationObjDB,
    OcdRelationDB,
    OcdPropertyClassDB,
    OcdArticleTaxesDB,
    OcdTaxSchemeDB,
    OcdPackagingDB,
)
from sqlalchemy.orm import Session
import logging
from ofml_import import util

logger = logging.getLogger("merge_ocd")
memoize_insert = util.memoize_insert


class InsertOcd:

    @memoize_insert("ocd_packaging")
    def extract_packaging(self, article_id: int) -> OcdPackagingDB:
        stmt = select(OcdPackagingDB).where(OcdPackagingDB.article_id == article_id)
        ocd_packaging_db = self.session.execute(stmt).scalar()
        ocd_packaging = util.copy_orm_object(ocd_packaging_db, no_ids=True)
        return ocd_packaging

    @memoize_insert("ocd_taxscheme")
    def extract_tax_scheme(self, tax_id: int) -> OcdTaxSchemeDB:
        stmt = select(OcdTaxSchemeDB).where(OcdTaxSchemeDB.id == tax_id)
        ocd_taxscheme_db = self.session.execute(stmt).scalar()
        ocd_taxscheme = util.copy_orm_object(ocd_taxscheme_db, no_ids=True)
        return ocd_taxscheme

    @memoize_insert("ocd_articletaxes")
    def extract_article_taxes(self, article_id: int) -> list[OcdArticleTaxesDB]:
        stmt = select(OcdArticleTaxesDB).where(
            OcdArticleTaxesDB.article_id == article_id
        )
        ocd_articletaxes_list_db = self.session.execute(stmt).scalars().all()
        ocd_articletaxes_list = [
            util.copy_orm_object(_, no_ids=True) for _ in ocd_articletaxes_list_db
        ]
        for t, t_db in zip(ocd_articletaxes_list, ocd_articletaxes_list_db):
            t.ref_taxscheme = self.extract_tax_scheme(t_db.tax_id)
        return ocd_articletaxes_list

    @memoize_insert("ocd_propertyvalue")
    def extract_property_value(self, property_id: str) -> list[OcdPropertyValueDB]:
        stmt = select(OcdPropertyValueDB).where(
            OcdPropertyValueDB.property_id == property_id
        )
        ocd_propertyvalue_list_db = self.session.execute(stmt).scalars().all()
        ocd_propertyvalue_list = [
            util.copy_orm_object(_, no_ids=True) for _ in ocd_propertyvalue_list_db
        ]

        for p, p_db in zip(ocd_propertyvalue_list, ocd_propertyvalue_list_db):
            p.ref_text = self.extract_text(p_db.text_id)
            p.ref_relationobj = self.extract_relationobj(p_db.relobj_id)
        return ocd_propertyvalue_list

    @memoize_insert("ocd_property")
    def extract_property(self, prop_class_id: int) -> list[OcdPropertyDB]:
        stmt = select(OcdPropertyDB).where(
            OcdPropertyDB.property_class_id == prop_class_id
        )
        ocd_property_list_db = self.session.execute(stmt).scalars().all()
        ocd_property_list = [
            util.copy_orm_object(_, no_ids=True) for _ in ocd_property_list_db
        ]
        for p, p_db in zip(ocd_property_list, ocd_property_list_db):
            p.ref_text = self.extract_text(p_db.text_id)
            p.ref_text_hint = self.extract_text(p_db.text_hint_id)
            p.ref_relationobj = self.extract_relationobj(p_db.relobj_id)
            p.ref_property_value = self.extract_property_value(p_db.id)
        return ocd_property_list

    @memoize_insert("ocd_propertyclass")
    def extract_propertyclass_(self, prop_class_id: int) -> OcdPropertyClassDB:
        stmt = select(OcdPropertyClassDB).where(OcdPropertyClassDB.id == prop_class_id)
        ocd_propertyclass_db = self.session.execute(stmt).scalar_one()
        text_id = ocd_propertyclass_db.text_id
        ocd_propertyclass = util.copy_orm_object(ocd_propertyclass_db, no_ids=True)
        ocd_propertyclass.ref_text = self.extract_text(text_id)
        ocd_propertyclass.ref_properties = self.extract_property(prop_class_id)
        # # set reference pclass on every pvalue, otherweise integrity error because no relationship
        # for prop in ocd_propertyclass.ref_properties:
        #     for pval in prop.ref_property_value:
        #         pval.ref_property_class = ocd_propertyclass
        return ocd_propertyclass

    def extract_propertyclass(self, article_id: int) -> list[OcdPropertyClassDB]:
        stmt = select(OcdArticlePropertyclassAssocDB).where(
            OcdArticlePropertyclassAssocDB.article_id == article_id
        )
        ocd_propertyclass_list_db = self.session.execute(stmt).scalars().all()
        ocd_propertyclass_list = [
            self.extract_propertyclass_(p.propertyclass_id)
            for p in ocd_propertyclass_list_db
        ]
        return ocd_propertyclass_list

    @memoize_insert("ocd_relation")
    def extract_relation(self, relation_id: int) -> OcdRelationDB:
        stmt = select(OcdRelationDB).where(OcdRelationDB.id == relation_id)
        ocd_relation_db = self.session.execute(stmt).scalar()
        ocd_relation = util.copy_orm_object(ocd_relation_db, no_ids=True)
        return ocd_relation

    def extract_relationobj_relation_assoc(
        self, relobj_id: int
    ) -> OcdRelationObjRelationAssocDB:
        stmt_assoc = select(OcdRelationObjRelationAssocDB).where(
            OcdRelationObjRelationAssocDB.relationobj_id == relobj_id
        )
        ocd_relationobj_assoc_list_db = self.session.execute(stmt_assoc).scalars().all()
        ocd_relationobj_assoc_list = [
            util.copy_orm_object(_, no_ids=True) for _ in ocd_relationobj_assoc_list_db
        ]

        for rel_assoc, rel_assoc_db in zip(
            ocd_relationobj_assoc_list, ocd_relationobj_assoc_list_db
        ):
            rel_assoc.ref_relation = self.extract_relation(rel_assoc_db.id)

        return ocd_relationobj_assoc_list

    @memoize_insert("ocd_relationobj")
    def extract_relationobj(self, relobj_id: int) -> OcdRelationObjDB:
        if relobj_id is None:
            return None
        stmt = select(OcdRelationObjDB).where(OcdRelationObjDB.id == relobj_id)
        ocd_relationobj_db = self.session.execute(stmt).scalar()
        ocd_relationobj = util.copy_orm_object(ocd_relationobj_db, no_ids=True)

        ocd_relationobj.ref_relationobj_relation_assoc = (
            self.extract_relationobj_relation_assoc(relobj_id)
        )

        return ocd_relationobj

    @memoize_insert("ocd_price")
    def extract_price(self, article_id: int) -> list[OcdPriceDB]:
        stmt = select(OcdPriceDB).where(OcdPriceDB.article_id == article_id)
        ocd_price_list_db = self.session.execute(stmt).scalars().all()
        ocd_price_list = util.copy_orm_object(ocd_price_list_db, no_ids=True)
        for ocd_price, ocd_price_db in zip(ocd_price_list, ocd_price_list_db):
            ocd_price.ref_text = self.extract_text(ocd_price_db.price_text_id)
        return ocd_price_list

    @memoize_insert("ocd_text")
    def extract_text(self, text_id: int) -> OcdTextDB | None:
        if text_id is None:
            return None
        stmt = select(OcdTextDB).where(OcdTextDB.id == text_id)
        ocd_text_db = self.session.execute(stmt).scalar()
        ocd_text = util.copy_orm_object(ocd_text_db, no_ids=True)
        ocd_text.ref_program = self.merge_program
        return ocd_text

    @memoize_insert("ocd_artbase")
    def extract_artbase(self, article_id: int) -> list[OcdArtbaseDB]:
        stmt = select(OcdArtbaseDB).where(OcdArtbaseDB.article_id == article_id)
        ocd_artbase_list_db = self.session.execute(stmt).scalars().all()
        ocd_artbase_list = util.copy_orm_object(ocd_artbase_list_db, no_ids=True)
        return ocd_artbase_list

    def get_article(self, article_nr: str, program: str) -> OcdArticleDB:
        article = self.session.execute(
            select(OcdArticleDB)
            .join(OcdProgramDB)
            .where(
                and_(
                    OcdArticleDB.article_nr == article_nr,
                    OcdProgramDB.name == program,
                )
            )
        ).scalar_one()
        return article

    def __init__(
        self,
        articlenumbers: list[str],
        program: str,
        session: Session,
        merge_program: OcdProgramDB,
    ):

        self.identy_map_by_key = defaultdict(dict)
        self.session = session
        self.merge_program = merge_program

        for article_nr in articlenumbers:

            article: OcdArticleDB = self.get_article(article_nr, program)

            article_copy = util.copy_orm_object(article)
            print("INSERT ... article_copy.....")
            print(article_copy.article_nr)

            article_copy.ref_short_text = self.extract_text(article.short_text_id)
            article_copy.ref_long_text = self.extract_text(article.long_text_id)
            article_copy.ref_artbase = self.extract_artbase(article.id)
            article_copy.ref_price = self.extract_price(article.id)

            article_copy.ref_relationobj = self.extract_relationobj(
                article.relobj_id,
            )

            article_copy.ref_propertyclasses = self.extract_propertyclass(article.id)
            article_copy.ref_articletaxes = self.extract_article_taxes(article.id)
            article_copy.ref_packaging = self.extract_packaging(article.id)

            article_copy.ref_program = self.merge_program

            input("article copied.")

            session.add(article_copy)

            session.commit()
            print(article_copy)


def ofml2dbscheme(
    session: Session, merge_program: OcdProgramDB, articles: list[ArticleProgram]
):

    program2articles = itertools.groupby(articles, lambda a: a.program)
    for program, articles in program2articles:
        InsertOcd(
            articlenumbers=[a.article_nr for a in articles],
            program=program,
            session=session,
            merge_program=merge_program,
        )


if __name__ == "__main__":

    from models import new_session, engine

    session = new_session()  # next(generate_session())
    article = session.get_one(OcdArticleDB, 1)

    articles = [
        ArticleProgram(article_nr="JDBDCN20C", program="jet3"),
        ArticleProgram(article_nr="JDBDCN20E", program="jet3"),
        ArticleProgram(article_nr="S6APV16450A", program="s6"),
        ArticleProgram(article_nr="S6APV16450B2", program="s6"),
    ]
    from models import new_session

    session = new_session()  # next(generate_session())
    ofml2dbscheme(session, 6, articles)
