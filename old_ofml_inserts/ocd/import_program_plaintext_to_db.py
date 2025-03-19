from collections import defaultdict
import functools
from typing import DefaultDict
import pandas as pd
from pprint import pprint
from ofml_import.text_util import get_language_2_text
from models.ocd import (
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
from ofml_api.repository import OFMLPart
import logging

logger = logging.getLogger("inser_ocd")


def format_text_table(df: pd.DataFrame):
    df.loc[df["text"].isna(), "text"] = ""
    return df


def extract_text(
    text_df: pd.DataFrame, multi: bool, text_type: TextType, program: OcdProgramDB
):
    language2text = get_language_2_text(text_df, multi)
    return OcdTextDB(
        text_type=text_type,
        text_de=language2text["de"],
        text_en=language2text["en"],
        text_fr=language2text["fr"],
        text_nl=language2text["nl"],
        ref_program=program,
    )


# def memoize_insert(table_name: str):
#     def decorator(func):
#         @functools.wraps(func)
#         def wrapper(self, *args, **kwargs):
#             cache = self.identy_map_by_key[table_name]

#             key = make_insert_key(*args, **kwargs)
#             if key in cache:
#                 return cache[key]
#             result = func(self, *args, **kwargs)
#             cache[key] = result
#             return result

#         return wrapper

#     return decorator


# def make_insert_key(*keys):
#     return "::".join(map(str, keys))


class InsertOcd:

    def assert_not_extracted(self, result: pd.DataFrame):
        assert result["db_table_id"].any() == False

    def set_extracted(self, origin_df: pd.DataFrame, this_df: pd.DataFrame):
        self.assert_not_extracted(origin_df.loc[this_df.index])
        origin_df.loc[this_df.index, "db_table_id"] = 1

    @memoize_insert("ocd_packaging")
    def extract_packaging(self, article_nr: str) -> OcdPackagingDB:
        df = self.ocd_packaging.df
        result = df[df["article_nr"] == article_nr]

        if result.empty:
            logger.warning(f"{article_nr} yield no packaging")
            return None

        assert result.shape[0] == 1

        row = result.iloc[0]

        self.set_extracted(df, result)
        return OcdPackagingDB(
            var_cond=row.var_cond,
            width=row.width,
            height=row.height,
            depth=row.depth,
            measure_unit=row.measure_unit,
            volume=row.volume,
            tara_weight=row.tara_weight,
            net_weight=row.net_weight,
            weight_unit=row.weight_unit,
            items_per_unit=row.items_per_unit,
            pack_units=row.pack_units,
        )

    def extract_global_packaging(self) -> list[OcdGlobalPackagingDB]:
        df = self.ocd_packaging.df
        result = df[df["article_nr"] == "*"]

        if result.empty:
            logger.warning(f"no global packaging found with wildcard *")
            return []

        self.set_extracted(df, result)
        return result.apply(
            lambda row: OcdGlobalPackagingDB(
                var_cond=row.var_cond,
                width=row.width,
                height=row.height,
                depth=row.depth,
                measure_unit=row.measure_unit,
                volume=row.volume,
                tara_weight=row.tara_weight,
                net_weight=row.net_weight,
                weight_unit=row.weight_unit,
                items_per_unit=row.items_per_unit,
                pack_units=row.pack_units,
                ref_program=self.program,
            ),
            axis=1,
        )

    @memoize_insert("ocd_taxscheme")
    def extract_tax_scheme(self, tax_id: str) -> OcdTaxSchemeDB:
        df = self.ocd_taxscheme.df
        result = df[df["tax_id"] == tax_id]

        if result.empty:
            logger.warning(f"{tax_id} yield no taxtscheme")
            return None

        assert result.shape[0] == 1

        row = result.iloc[0]

        self.set_extracted(df, result)
        return OcdTaxSchemeDB(
            country=row.country,
            region=row.region,
            number=int(row.number),
            tax_type=row.tax_type,
            tax_category=row.tax_category,
        )

    @memoize_insert("ocd_articletaxes")
    def extract_article_taxes(self, article_nr: str) -> list[OcdArticleTaxesDB]:
        df = self.ocd_articletaxes.df
        result = df[df["article_nr"] == article_nr]

        if result.empty:
            logger.warning(f"{article_nr} yield no articletaxes")
            return []

        self.set_extracted(df, result)
        return result.apply(
            lambda row: OcdArticleTaxesDB(
                date_from=row.date_from,
                date_to=row.date_to,
                ref_taxscheme=self.extract_tax_scheme(row.tax_id),
            ),
            axis=1,
        ).to_list()

    @memoize_insert("ocd_propertyvalue")
    def extract_property_value(
        self, prop_class: str, property: str
    ) -> list[OcdPropertyValueDB]:
        df = self.ocd_propertyvalue.df
        result = df[(df["prop_class"] == prop_class) & (df["property"] == property)]
        self.set_extracted(self.ocd_propertyvalue.df, result)
        return result.apply(
            lambda row: OcdPropertyValueDB(
                pos_pval=row.pos_pval,
                is_default=row.is_default,
                suppress_txt=row.suppress_txt,
                op_from=row.op_from,
                value_from=row.value_from,
                op_to=row.op_to,
                value_to=row.value_to,
                raster=row.raster,
                ref_text=self.extract_propvalue_text(row.pval_textnr),
                ref_relationobj=self.extract_relationobj(row.rel_obj),
            ),
            axis=1,
        ).to_list()

    @memoize_insert("ocd_property")
    def extract_property(self, prop_class: str) -> list[OcdPropertyDB]:
        df = self.ocd_property.df
        result = df[df["prop_class"] == prop_class]
        self.set_extracted(self.ocd_property.df, result)
        return result.apply(
            lambda row: OcdPropertyDB(
                property=row.property,
                pos_prop=row.pos_prop,
                prop_type=row.prop_type,
                digits=row.digits,
                dec_digits=row.dec_digits,
                need_input=row.need_input,
                add_values=row.add_values,
                restrictable=row.restrictable,
                multi_option=row.multi_option,
                scope=row.scope,
                txt_control=row.txt_control,
                ref_text=self.extract_property_text(row.prop_textnr),
                ref_text_hint=self.extract_prophint_text(row.hint_text_id),
                ref_relationobj=self.extract_relationobj(row.rel_obj),
                ref_property_value=self.extract_property_value(
                    row.prop_class, row.property
                ),
            ),
            axis=1,
        ).to_list()

    @memoize_insert("ocd_propertyclass")
    def extract_propertyclass_(self, prop_class: str) -> OcdPropertyClassDB:
        df = self.ocd_propertyclass.df
        row = df[df["prop_class"] == prop_class].iloc[0]
        orm = OcdPropertyClassDB(
            pos_class=int(row.pos_class),
            prop_class=row.prop_class,
            ref_text=self.extract_propclass_text(row.textnr),
            ref_properties=self.extract_property(row.prop_class),
        )
        # # set reference pclass on every pvalue, otherweise integrity error because no relationship
        # for prop in orm.ref_properties:
        #     for pval in prop.ref_property_value:
        #         pval.ref_property_class = orm
        return orm

    def extract_propertyclass(self, article_nr: str) -> list[OcdPropertyClassDB]:
        df = self.ocd_propertyclass.df
        result = df[df["article_nr"] == article_nr]
        self.set_extracted(self.ocd_propertyclass.df, result)

        # assert not result.empty, f"{article_nr} yield no propertyclass"
        if result.empty:
            logger.warning(f"{article_nr} yield no propertyclass")
            return []
        return result.apply(
            lambda row: self.extract_propertyclass_(row.prop_class),
            axis=1,
        ).to_list()

    @memoize_insert("ocd_relation")
    def extract_relation(self, rel_name: str) -> OcdRelationDB:
        df = self.ocd_relation.df
        result = df[df["rel_name"] == rel_name]
        b = "\n".join(result["rel_block"].dropna())
        self.set_extracted(self.ocd_relation.df, result)
        return OcdRelationDB(name=rel_name, rel_block=b)

    @memoize_insert("ocd_relationobj")
    def extract_relationobj(self, rel_obj: str) -> OcdRelationObjDB:
        df = self.ocd_relationobj.df
        result = df[df["rel_obj"] == rel_obj]

        if result.empty:
            return None

        assert not result.empty, f"ocd_relationobj didnt yield rows for {rel_obj}"

        self.set_extracted(self.ocd_relationobj.df, result)

        orm = OcdRelationObjDB(
            name=str(rel_obj),
        )

        orm.ref_relationobj_relation_assoc = result.apply(
            lambda row: OcdRelationObjRelationAssocDB(
                position=row.position,
                rel_type=row.rel_type,
                rel_domain=row.rel_domain,
                ref_relationobj=orm,
                ref_relation=self.extract_relation(row.rel_name),
            ),
            axis=1,
        ).to_list()
        assert len(
            orm.ref_relationobj_relation_assoc
        ), f"{rel_obj} did yield no relations"

        return orm

    @memoize_insert("ocd_price")
    def extract_price(self, article_nr: str) -> list[OcdPriceDB]:
        df = self.ocd_price.df
        result = df[df["article_nr"] == article_nr]
        self.set_extracted(df, result)
        return result.apply(
            lambda row: OcdPriceDB(
                var_cond=row.var_cond,
                price_type=row.price_type,
                price_level=row.price_level,
                price=row.price,
                is_fix=row.is_fix,
                currency=row.currency,
                date_from=row.date_from,
                date_to=row.date_to,
                scale_quantity=row.scale_quantity,
                ref_text=self.extract_price_text(row.price_textnr),
            ),
            axis=1,
        ).to_list()

    @memoize_insert("ocd_propvaluetext")
    def extract_propvalue_text(self, pvalue_textnr: str):
        df = self.ocd_propvaluetext.df
        result = df.loc[lambda df: df["textnr"] == pvalue_textnr]
        if result.empty:
            return None
        self.set_extracted(df, result)
        return extract_text(
            result, multi=False, text_type=TextType.PROPVALUE, program=self.program
        )

    @memoize_insert("ocd_propertytext")
    def extract_property_text(self, prop_textnr: str):
        df = self.ocd_propertytext.df
        result = df.loc[lambda df: df["textnr"] == prop_textnr]
        if result.empty:
            return None
        self.set_extracted(df, result)
        return extract_text(
            result, multi=False, text_type=TextType.PROP, program=self.program
        )

    @memoize_insert("ocd_prophinttext")
    def extract_prophint_text(self, prop_textnr: str):
        df = self.ocd_prophinttext.df
        result = df.loc[lambda df: df["textnr"] == prop_textnr]
        if result.empty:
            return None
        self.set_extracted(df, result)
        return extract_text(
            result, multi=False, text_type=TextType.PROPHINT, program=self.program
        )

    @memoize_insert("ocd_propclasstext")
    def extract_propclass_text(self, propclass_textnr: str):
        df = self.ocd_propclasstext.df
        result = df.loc[lambda df: df["textnr"] == propclass_textnr]
        if result.empty:
            return None
        self.set_extracted(df, result)
        return extract_text(
            result, multi=False, text_type=TextType.PROPCLASS, program=self.program
        )

    def extract_usermessage(self) -> list[OcdTextDB]:
        df = self.ocd_usermessage.df
        if df.empty:
            return []
        self.set_extracted(df, df)
        return (
            df.groupby(
                "textnr",
            )
            .apply(
                lambda group_df: extract_text(
                    group_df,
                    multi=True,
                    text_type=TextType.USERMESSAGE,
                    program=self.program,
                ),
            )
            .to_list()
        )

    @memoize_insert("ocd_artshorttext")
    def extract_artshort_text(self, short_textnr: str):
        assert short_textnr
        df = self.ocd_artshorttext.df
        result = df.loc[lambda df: df["textnr"] == short_textnr]
        if result.empty:
            return None
        assert not result.empty
        self.set_extracted(df, result)
        return extract_text(
            result, multi=False, text_type=TextType.SHORT, program=self.program
        )

    @memoize_insert("ocd_pricetext")
    def extract_price_text(self, price_textnr: str) -> OcdTextDB:
        df = self.ocd_pricetext.df
        result = df.loc[lambda df: df["textnr"] == price_textnr]
        if result.empty:
            return None
        self.set_extracted(df, result)
        return extract_text(
            result, multi=False, text_type=TextType.PRICE, program=self.program
        )

    @memoize_insert("ocd_artlongtext")
    def extract_artlong_text(self, long_textnr: str):
        df = self.ocd_artlongtext.df
        result = df.loc[lambda df: df["textnr"] == long_textnr]
        if result.empty:
            return None
        self.set_extracted(df, result)
        return extract_text(
            result, multi=True, text_type=TextType.LONG, program=self.program
        )

    @memoize_insert("ocd_artbase")
    def extract_artbase(self, article_nr: str):
        df = self.ocd_artbase.df
        result = df[df["article_nr"] == article_nr]
        self.set_extracted(df, result)
        return result.apply(
            lambda row: OcdArtbaseDB(
                class_name=row.prop_class,
                prop_name=row.property,
                prop_value=row.prop_value,
            ),
            axis=1,
        ).to_list()

    def ocd_tablename2df(self) -> dict[str, pd.DataFrame]:
        return {k: self.__dict__[k].df for k in self.__dict__ if k.startswith("ocd_")}

    def assert_all_inserted(self):
        ocd_tablename2df = self.ocd_tablename2df()
        for table_name, df in ocd_tablename2df.items():
            df_null = df.loc[df["db_table_id"].isnull()]
            if not df_null.empty:
                print(df_null.head().to_string())
            assert (
                df_null.empty
            ), f"table {table_name} has no inserted rows: {df_null.shape}"

            print(f"table {table_name} all inserted OK")

    def extract_rows_without_link(self) -> list[OcdTextDB]:
        print("extract_rows_without_link.....")
        orm_list_all = []
        for table, extract_function, col_name_key in [
            (self.ocd_artshorttext, self.extract_artshort_text, "textnr"),
            (self.ocd_artlongtext, self.extract_artlong_text, "textnr"),
            (self.ocd_propclasstext, self.extract_propclass_text, "textnr"),
            (self.ocd_propertytext, self.extract_property_text, "textnr"),
            (self.ocd_propvaluetext, self.extract_propvalue_text, "textnr"),
            (self.ocd_prophinttext, self.extract_prophint_text, "textnr"),
            (self.ocd_pricetext, self.extract_price_text, "textnr"),
            (self.ocd_relationobj, self.extract_relationobj, "rel_obj"),
            (
                self.ocd_relation,
                self.extract_relation,
                "rel_name",
            ),  # EXTRACTION DONE VIA RELATION_OBJ
            (self.ocd_taxscheme, self.extract_tax_scheme, "tax_id"),
        ]:

            df_null = table.df.loc[table.df["db_table_id"].isnull()]

            # print(df_null.to_string())
            # print("df_null..", df_null.shape)

            orm_list = [extract_function(key) for key in df_null[col_name_key].unique()]
            orm_list_all.extend(orm_list)
        print("orm_list_all....", len(orm_list_all))

        return orm_list_all

    def __init__(
        self,
        ocd: OFMLPart,
        session: Session,
        program_name: str,
        description: str | None = None,
    ):
        self.program = OcdProgramDB(
            name=program_name, import_path=str(ocd.path), description=description
        )

        self.identy_map_by_key = defaultdict(dict)

        self.ocd_article = ocd.table("ocd_article.csv")
        self.ocd_artshorttext = ocd.table("ocd_artshorttext.csv")
        self.ocd_artlongtext = ocd.table("ocd_artlongtext.csv")
        self.ocd_artbase = ocd.table("ocd_artbase.csv")
        self.ocd_price = ocd.table("ocd_price.csv")
        self.ocd_pricetext = ocd.table("ocd_pricetext.csv")
        self.ocd_relationobj = ocd.table("ocd_relationobj.csv")
        self.ocd_relation = ocd.table("ocd_relation.csv")
        self.ocd_propertyclass = ocd.table("ocd_propertyclass.csv")
        self.ocd_propclasstext = ocd.table("ocd_propclasstext.csv")
        self.ocd_property = ocd.table("ocd_property.csv")
        self.ocd_propertytext = ocd.table("ocd_propertytext.csv")
        self.ocd_prophinttext = ocd.table("ocd_prophinttext.csv")
        self.ocd_propertyvalue = ocd.table("ocd_propertyvalue.csv")
        self.ocd_propvaluetext = ocd.table("ocd_propvaluetext.csv")
        self.ocd_articletaxes = ocd.table("ocd_articletaxes.csv")
        self.ocd_taxscheme = ocd.table("ocd_taxscheme.csv")
        self.ocd_packaging = ocd.table("ocd_packaging.csv")
        self.ocd_usermessage = ocd.table("ocd_usermessage.csv")

        for table in [self.ocd_artlongtext, self.ocd_usermessage]:
            table.df = format_text_table(table.df)

        usermessage_list = self.extract_usermessage()
        session.add_all(usermessage_list)
        global_packaging_list = self.extract_global_packaging()
        session.add_all(global_packaging_list)

        for row in self.ocd_article.df.itertuples():

            print("INSERT article", row.article_nr, program_name)

            article = OcdArticleDB(
                article_nr=row.article_nr,
                art_type=row.art_type,
                manufacturer=row.manufacturer,
                series=row.series,
                fast_supply=row.fast_supply,
                discountable=row.discountable,
                order_unit=row.order_unit,
                ref_short_text=self.extract_artshort_text(row.short_textnr),
                ref_long_text=self.extract_artlong_text(row.long_textnr),
                ref_artbase=self.extract_artbase(row.article_nr),
                ref_price=self.extract_price(row.article_nr),
                ref_relationobj=self.extract_relationobj(
                    row.rel_obj,
                ),
                ref_propertyclasses=self.extract_propertyclass(row.article_nr),
                ref_articletaxes=self.extract_article_taxes(row.article_nr),
                ref_packaging=self.extract_packaging(row.article_nr),
                ref_program=self.program,
            )
            # assert self.ocd_artshorttext.df["db_table_id"].any()

            session.add(article)
            # session.flush()
            # session.commit()
            # print("commited 1 :)")
            self.identy_map_by_key["ocd_article"][article.article_nr] = article

        self.set_extracted(self.ocd_article.df, self.ocd_article.df)

        print("DONE.", program_name)
        # input(".")
        self.extract_rows_without_link()
        self.assert_all_inserted()
        session.commit()


def print_not_inserted_rows(df: pd.DataFrame):
    df_null = df.loc[df["db_table_id"].isnull()]
    if df_null.empty:
        print("EMPTY")
    else:
        print(df_null.shape)
        # print(df_null.to_string())


def ofml2dbscheme(
    ocd: OFMLPart,
    session: Session,
    program_name: str,
    description: str | None = None,
):
    InsertOcd(ocd, session, program_name, description)
