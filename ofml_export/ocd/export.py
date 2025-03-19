from pathlib import Path
import pandas as pd
from sqlalchemy.orm import Session, DeclarativeBase
from sqlalchemy import Engine
from models.ocd import (
    OcdArticleDB,
    OcdArticlePropertyclassAssocDB,
    OcdArticleTaxesDB,
    OcdGlobalPackagingDB,
    OcdPackagingDB,
    OcdPriceDB,
    OcdProgramDB,
    OcdPropertyClassDB,
    OcdRelationDB,
    OcdRelationObjDB,
    OcdRelationObjRelationAssocDB,
    OcdTaxSchemeDB,
    OcdTextDB,
    OcdRoundingDB,
    OcdArtbaseDB,
    OcdPropertyDB,
    OcdPropertyValueDB,
    TextType,
)
from models import engine
import ofml_export.ocd.formatting as formatter


class Db2Ocd:

    def __init__(self, program_name: str, engine: Engine) -> None:
        self.session = Session(engine)
        self.engine = engine
        self.program_name = program_name

    def read_sql(self, statement) -> pd.DataFrame:
        return pd.read_sql(
            statement,
            self.engine,
        )

    def extract_table_by_ids(
        self, table: DeclarativeBase, id_attr: str, ids: list[int]
    ):
        return self.read_sql(
            self.session.query(table).filter(getattr(table, id_attr).in_(ids)).statement
        )

    def extract_ocd_relation(self, relation_ids: list[int]):
        return self.extract_table_by_ids(OcdRelationDB, "id", relation_ids)

    def extract_ocd_relationobj(self, relationobj_ids: list[int]):
        df = self.read_sql(
            self.session.query(OcdRelationObjRelationAssocDB)
            .filter(OcdRelationObjRelationAssocDB.relationobj_id.in_(relationobj_ids))
            .statement
        )
        return df

    def extract_ocd_taxscheme(self, tax_ids: list[int]):
        return self.extract_table_by_ids(OcdTaxSchemeDB, "id", tax_ids)

    def extract_ocd_articletaxes(self, article_ids: list[int]):
        return self.extract_table_by_ids(OcdArticleTaxesDB, "article_id", article_ids)

    def extract_ocd_packaging(self, article_ids: list[int], program_id: int):

        global_packaging_df = self.read_sql(
            self.session.query(OcdGlobalPackagingDB)
            .filter(OcdGlobalPackagingDB.program_id == program_id)
            .statement
        )
        global_packaging_df["article_nr"] = "*"

        packaging_df = self.read_sql(
            self.session.query(
                OcdPackagingDB,
                OcdArticleDB.article_nr,
            )
            .join(
                OcdArticleDB,
                OcdArticleDB.id == OcdPackagingDB.article_id,
            )
            .filter(OcdPackagingDB.article_id.in_(article_ids))
            .statement
        )

        return pd.concat([global_packaging_df, packaging_df]).reset_index(drop=True)

    def extract_ocd_propertyvalue(self, property_ids: list[int]):
        df = self.read_sql(
            self.session.query(
                OcdPropertyValueDB,
                OcdPropertyClassDB.prop_class,
                OcdPropertyDB.property,
            )
            .join(
                OcdPropertyClassDB,
                OcdPropertyValueDB.property_class_id == OcdPropertyClassDB.id,
            )
            .join(
                OcdPropertyDB,
                OcdPropertyValueDB.property_id == OcdPropertyDB.id,
            )
            .filter(OcdPropertyValueDB.property_id.in_(property_ids))
            .statement
        )

        # print(df[df.columns[:]].to_string())
        # print(df.columns)
        # print(df.shape)
        return df

    def extract_ocd_property(self, propertyclass_ids: list[str]):
        df = self.read_sql(
            self.session.query(OcdPropertyDB, OcdPropertyClassDB.prop_class)
            .join(
                OcdPropertyDB,
                OcdPropertyDB.property_class_id == OcdPropertyClassDB.id,
            )
            .filter(OcdPropertyDB.property_class_id.in_(propertyclass_ids))
            .statement
        )

        # print(df[df.columns[:]].to_string())
        # print(df.columns)
        return df

    def extract_ocd_propertyclass(self, article_ids: list[str]):
        return self.read_sql(
            self.session.query(OcdPropertyClassDB, OcdArticleDB.article_nr)
            .join(
                OcdArticlePropertyclassAssocDB,
                OcdPropertyClassDB.id
                == OcdArticlePropertyclassAssocDB.propertyclass_id,
            )
            .join(
                OcdArticleDB,
                OcdArticleDB.id == OcdArticlePropertyclassAssocDB.article_id,
            )
            .filter(OcdArticleDB.id.in_(article_ids))
            .statement
        )

    def extract_ocd_artbase(self, article_ids: list[int]):
        return self.read_sql(
            self.session.query(OcdArtbaseDB, OcdArticleDB.article_nr)
            .join(OcdArticleDB, OcdArticleDB.id == OcdArtbaseDB.article_id)
            .filter(OcdArtbaseDB.article_id.in_(article_ids))
            .statement
        )

    def extract_ocd_text_by_type(self, program_id: int, text_type: TextType):
        df = self.read_sql(
            self.session.query(OcdTextDB)
            .filter(
                OcdTextDB.program_id == program_id, OcdTextDB.text_type == text_type
            )
            .statement
        )
        # fmt_ocd_text(df)
        return df

    def extract_ocd_text_by_ids(self, text_ids: list[int]):
        df = self.read_sql(
            self.session.query(OcdTextDB).filter(OcdTextDB.id.in_(text_ids)).statement
        )
        # fmt_ocd_text(df)
        return df

    def extract_ocd_rounding(self, rounding_ids: list[int]):
        return self.read_sql(
            self.session.query(OcdRoundingDB)
            .filter(OcdRoundingDB.id.in_(rounding_ids))
            .statement
        )

    def extract_ocd_price(self, article_ids: list[str]):
        df = self.read_sql(
            self.session.query(OcdPriceDB, OcdArticleDB.article_nr)
            .join(OcdArticleDB, OcdArticleDB.id == OcdPriceDB.article_id)
            .filter(OcdPriceDB.article_id.in_(article_ids))
            .statement
        )
        return df

    def extract_ocd_article_df(self, program_id: int):

        df = self.read_sql(
            self.session.query(OcdArticleDB)
            .filter(OcdArticleDB.program_id == program_id)
            .statement
        )

        # print(df.to_string())
        return df

    def dbscheme2ocd(
        self,
    ):
        session = self.session
        program = (
            session.query(OcdProgramDB)
            .filter(OcdProgramDB.name == self.program_name)
            .one()
        )

        ocd_article_df = self.extract_ocd_article_df(program.id)
        article_ids = ocd_article_df["id"].to_list()

        ocd_articletaxes_df = self.extract_ocd_articletaxes(article_ids)
        ocd_taxscheme_df = self.extract_ocd_taxscheme(
            ocd_articletaxes_df["tax_id"].to_list()
        )
        ocd_packaging_df = self.extract_ocd_packaging(article_ids, program.id)
        ocd_artshorttext_df = self.extract_ocd_text_by_type(program.id, TextType.SHORT)
        print("ocd_artshorttext_df...", ocd_artshorttext_df.shape)
        ocd_artlongtext_df = self.extract_ocd_text_by_ids(
            ocd_article_df["long_text_id"].to_list()
        )
        ocd_price_df = self.extract_ocd_price(article_ids)
        ocd_price_text_df = self.extract_ocd_text_by_ids(
            ocd_price_df["price_text_id"].to_list()
        )
        ocd_rounding_df = self.extract_ocd_rounding(
            ocd_price_df["rounding_id"].to_list()
        )
        ocd_artbase_df = self.extract_ocd_artbase(article_ids)
        ocd_propertyclass_df = self.extract_ocd_propertyclass(article_ids)
        ocd_propclasstext_df = self.extract_ocd_text_by_ids(
            ocd_propertyclass_df["text_id"].to_list()
        )
        ocd_property_df = self.extract_ocd_property(
            ocd_propertyclass_df["id"].to_list()
        )
        ocd_propertytext_df = self.extract_ocd_text_by_ids(
            ocd_property_df["text_id"].to_list()
        )
        ocd_prophinttext_df = self.extract_ocd_text_by_ids(
            ocd_property_df["text_hint_id"].to_list()
        )
        ocd_propertyvalue_df = self.extract_ocd_propertyvalue(
            ocd_property_df["id"].to_list()
        )
        ocd_propvaluetext_df = self.extract_ocd_text_by_ids(
            ocd_propertyvalue_df["text_id"].to_list()
        )
        ocd_usermessage_df = self.extract_ocd_text_by_type(
            program.id, TextType.USERMESSAGE
        )

        ocd_relationobj_df = self.extract_ocd_relationobj(
            pd.concat(
                [
                    ocd_article_df["relobj_id"],
                    ocd_propertyclass_df["relobj_id"],
                    ocd_property_df["relobj_id"],
                    ocd_propertyvalue_df["relobj_id"],
                ]
            )
            .unique()
            .tolist()
        )

        ocd_relation_df = self.extract_ocd_relation(
            ocd_relationobj_df["relation_id"].unique().tolist()
        )
        print("export...")
        self.export(
            "ocd_export",
            {
                "ocd_article.csv": formatter.fmt_ocd_article(ocd_article_df),
                "ocd_articletaxes.csv": formatter.fmt_ocd_articletaxes(
                    ocd_articletaxes_df
                ),
                "ocd_taxscheme.csv": formatter.fmt_ocd_taxscheme(ocd_taxscheme_df),
                "ocd_packaging.csv": formatter.fmt_ocd_packaging(ocd_packaging_df),
                "ocd_artshorttext.csv": formatter.fmt_ocd_text(ocd_artshorttext_df),
                "ocd_artlongtext.csv": formatter.fmt_ocd_text(ocd_artlongtext_df),
                "ocd_price.csv": formatter.fmt_ocd_price(ocd_price_df),
                "ocd_pricetext.csv": formatter.fmt_ocd_text(ocd_price_text_df),
                "ocd_rounding.csv": formatter.fmt_ocd_rounding(ocd_rounding_df),
                "ocd_artbase.csv": formatter.fmt_ocd_artbase(ocd_artbase_df),
                "ocd_propertyclass.csv": formatter.fmt_ocd_propertyclass(
                    ocd_propertyclass_df
                ),
                "ocd_propclasstext.csv": formatter.fmt_ocd_text(ocd_propclasstext_df),
                "ocd_property.csv": formatter.fmt_ocd_property(ocd_property_df),
                "ocd_propertytext.csv": formatter.fmt_ocd_text(ocd_propertytext_df),
                "ocd_prophinttext.csv": formatter.fmt_ocd_text(ocd_prophinttext_df),
                "ocd_propertyvalue.csv": formatter.fmt_ocd_propertyvalue(
                    ocd_propertyvalue_df
                ),
                "ocd_propvaluetext.csv": formatter.fmt_ocd_text(ocd_propvaluetext_df),
                "ocd_usermessage.csv": formatter.fmt_ocd_text(ocd_usermessage_df),
                "ocd_relationobj.csv": formatter.fmt_ocd_relationobj(
                    ocd_relationobj_df
                ),
                "ocd_relation.csv": formatter.fmt_ocd_relation(ocd_relation_df),
                # TODO: optional/empty/not used
                "ocd_classification.csv": pd.DataFrame(),
                "ocd_codescheme.csv": pd.DataFrame(),
            },
        )

    def export(self, path: str | Path, fname2df: dict[str, pd.DataFrame]):
        path = Path(path)

        if path.exists():
            import shutil

            shutil.rmtree(path)
        path.mkdir()

        fname2df["ocd_version.csv"] = self.make_ocd_version_df(fname2df.keys())

        for fname, df in fname2df.items():
            df.to_csv(path / fname, header=False, sep=";", index=False)

    def make_ocd_version_df(self, fnames: list[str]):
        return pd.DataFrame(
            data={
                "version": "4.1",
                "rel_language": "SAP_4_6",
                "version2": "2.21.0",
                "timestamp1": "20060801",
                "timestamp2": "99991231",
                "language": "DE",
                "col_unknown_1": "",
                "col_unknown_2": "0",
                "tables": ",".join([fname[4:-4] for fname in fnames] + ["version"]),
                "col_unknown_3": "",
            },
            index=[0],
        )


def dbscheme2ocd(program_name: str):
    Db2Ocd(program_name, engine).dbscheme2ocd()


dbscheme2ocd("workplace")
