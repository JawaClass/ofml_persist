from sqlalchemy.orm import Session

from models.ocd import OcdArticleDB
from models import engine


def deepcopy_article(program_id: int, article_nr: str, session: Session):

    article = (
        session.query(OcdArticleDB).filter(OcdArticleDB.article_nr == article_nr).one()
    )

    print("article.... deepcopy....", article_nr)
    print(article)
    print("\nSHORT_TEXT:::")
    print(article.ref_short_text)
    print("\nLONG_TEXT:::")
    print(article.ref_long_text)
    print("\nRELATIONOBJ:::")
    print(article.ref_relationobj)
    print("\nARTBASE:::")
    print(article.ref_artbase)
    print("\nPRICE:::")
    print(article.ref_price)
    print("\nPROPERTYCLASSES:::")
    print(article.ref_propertyclasses)
    print("\nARTICLETAXES:::")
    print(article.ref_articletaxes)
    print("\nPACKAGING:::")
    print(article.ref_packaging)

    # article = OcdArticleDB(
    #             article_nr=row.article_nr,
    #             art_type=row.art_type,
    #             manufacturer=row.manufacturer,
    #             series=row.series,
    #             fast_supply=row.fast_supply,
    #             discountable=row.discountable,
    #             order_unit=row.order_unit,
    #             ref_short_text=self.extract_artshort_text(row.short_textnr),
    #             ref_long_text=self.extract_artlong_text(row.long_textnr),
    #             ref_artbase=self.extract_artbase(row.article_nr),
    #             ref_price=self.extract_price(row.article_nr),
    #             ref_relationobj=self.extract_relationobj(
    #                 row.rel_obj,
    #             ),
    #             ref_propertyclasses=self.extract_propertyclass(row.article_nr),
    #             ref_articletaxes=self.extract_article_taxes(row.article_nr),
    #             ref_packaging=self.extract_packaging(row.article_nr),
    #             ref_program=self.program,
    #         )


deepcopy_article(program_id=1, article_nr="WPAPTN", session=Session(engine))
