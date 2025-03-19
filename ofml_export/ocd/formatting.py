import pandas as pd
from ofml_export.ocd.ocd_table_scheme import (
    OCD_ARTICLE,
    OCD_ARTICLETAXES,
    OCD_PRICE,
    OCD_RELATION,
    OCD_TAXSCHEME,
    OCD_TEXT,
    OCD_ARTBASE,
    OCD_PROPERTYCLASS,
    OCD_PROPERTY,
    OCD_PROPERTYVALUE,
    OCD_PACKAGING,
    OCD_RELATIONOBJ,
)


def fmt_ocd_artbase(df: pd.DataFrame):
    df = df.rename(
        {
            "class_name": "prop_class",
            "prop_name": "property",
        },
        axis=1,
    )
    df = df[OCD_ARTBASE]
    return df


def fmt_ocd_article(df: pd.DataFrame):
    df = df.rename(
        {
            "short_text_id": "short_textnr",
            "long_text_id": "long_textnr",
            "relobj_id": "rel_obj",
        },
        axis=1,
    )
    df = df.drop(["program_id", "id"], axis=1)
    df = df[OCD_ARTICLE]
    return df


def fmt_ocd_rounding(df: pd.DataFrame):
    return df


def fmt_ocd_relation(df: pd.DataFrame):

    df["rel_block"] = df["rel_block"].str.split("\n")
    df = df.explode("rel_block")
    df = df.reset_index(drop=True)

    df["rel_blocknr"] = df.groupby(["name"]).cumcount() + 1

    df = df.rename(
        {
            "id": "rel_name",
            "relation_id": "rel_name",
        },
        axis=1,
    )

    df = df[OCD_RELATION]

    return df


def fmt_ocd_relationobj(df: pd.DataFrame):
    df = df.rename(
        {
            "relationobj_id": "rel_obj",
            "relation_id": "rel_name",
        },
        axis=1,
    )

    df = df[OCD_RELATIONOBJ]
    return df


def fmt_ocd_taxscheme(df: pd.DataFrame):
    df = df.rename(
        {
            "id": "tax_id",
        },
        axis=1,
    )
    df = df[OCD_TAXSCHEME]
    return df


def fmt_ocd_articletaxes(df: pd.DataFrame):
    df = df.rename(
        {
            "article_id": "article_nr",
        },
        axis=1,
    )
    df = df[OCD_ARTICLETAXES]
    return df


def fmt_ocd_packaging(df: pd.DataFrame):
    df = df[OCD_PACKAGING]
    return df


def fmt_ocd_propertyvalue(df: pd.DataFrame):
    df = df.rename(
        {
            "relobj_id": "rel_obj",
            "text_id": "pval_textnr",
        },
        axis=1,
    )
    df = df[OCD_PROPERTYVALUE]
    df.loc[df["rel_obj"].isna(), "rel_obj"] = 0
    return df


def fmt_ocd_property(df: pd.DataFrame):
    df = df.rename(
        {
            "relobj_id": "rel_obj",
            "text_id": "prop_textnr",
            "text_hint_id": "hint_text_id",
        },
        axis=1,
    )
    df = df[OCD_PROPERTY]
    return df


def fmt_ocd_propertyclass(df: pd.DataFrame):
    df = df.rename(
        {
            "text_id": "textnr",
            "relobj_id": "rel_obj",
        },
        axis=1,
    )
    df = df[OCD_PROPERTYCLASS]
    df.loc[df["rel_obj"].isna(), "rel_obj"] = 0
    return df


def fmt_ocd_price(df: pd.DataFrame):
    df = df.rename(
        {
            "price_text_id": "price_textnr",
        },
        axis=1,
    )
    df = df.drop(["article_id", "id"], axis=1)
    df = df[OCD_PRICE]
    return df


def fmt_ocd_text(df: pd.DataFrame):
    if df.empty:
        return pd.DataFrame()
    assert not df.empty
    df = df.rename(
        {
            "text_de": "de",
            "text_en": "en",
            "text_fr": "fr",
            "text_nl": "nl",
            "id": "textnr",
        },
        axis=1,
    )

    df = df.melt(
        value_vars=["de", "en", "fr", "nl"],
        var_name="language",
        value_name="text",
        id_vars=["textnr"],
    )

    df = (
        df.assign(text=df["text"].str.split("\n"))
        .explode("text")
        .reset_index(drop=True)
    )
    df["line_nr"] = df.groupby(["textnr", "language"]).cumcount() + 1
    df["line_fmt"] = "/"

    df = df[OCD_TEXT]
    df = df.sort_values(by=["textnr", "language"])
    # print(df.to_string())
    return df
