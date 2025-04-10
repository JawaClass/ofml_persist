from enum import Enum
import pandas as pd

from models.oap import ActionType
from ofml_export.oap.table_scheme import (
    OAP_ACTION,
    OAP_ACTIONCHOICE,
    OAP_ACTIONLIST,
    OAP_CREATEOBJ,
    OAP_DIMCHANGE,
    OAP_EXTMEDIA,
    OAP_IMAGE,
    OAP_INTERACTOR,
    OAP_ARTICLE2TYPE,
    OAP_METATYPE2TYPE,
    OAP_NUMTRIPEL,
    OAP_OBJECT,
    OAP_METHODCALL,
    OAP_MESSAGE,
    OAP_PROPCHANGE,
    OAP_PROPEDIT,
    OAP_PROPEDIT2,
    OAP_PROPEDITCLASSES,
    OAP_SYMBOLDISPLAY,
    OAP_TEXT,
    OAP_PROPEDITPROPS,
    OAP_TYPE,
    OAP_VERSION,
)
from ofml_export.util import col_enum_extract_value, fill_columns


def fmt_oap_interactor(df: pd.DataFrame):
    df = df.rename(
        {
            "name": "interactor",
        },
        axis=1,
    )
    df = fill_columns(df, OAP_INTERACTOR)
    df = df[OAP_INTERACTOR]
    df.loc[:, "symbol_type"] = col_enum_extract_value(df["symbol_type"])
    df.loc[:, "symbol_size"] = col_enum_extract_value(df["symbol_size"])
    return df


def fmt_oap_article2type(df: pd.DataFrame):
    df["type_id"] = df["name"]
    df = fill_columns(df, OAP_ARTICLE2TYPE)
    df = df[OAP_ARTICLE2TYPE]
    return df


def fmt_oap_metatype2type(df: pd.DataFrame):
    df["type_id"] = df["name"]
    df = fill_columns(df, OAP_METATYPE2TYPE)
    df = df[OAP_METATYPE2TYPE]
    return df


def fmt_oap_object(df: pd.DataFrame):
    df["id"] = df["name"]
    df = fill_columns(df, OAP_OBJECT)
    df = df[OAP_OBJECT]
    df.loc[:, "category"] = col_enum_extract_value(df["category"])
    return df


def fmt_oap_methodcall(df: pd.DataFrame):
    df["id"] = df["name"]
    df = fill_columns(df, OAP_METHODCALL)
    df = df[OAP_METHODCALL]
    df.loc[:, "type"] = col_enum_extract_value(df["type"])
    return df


def fmt_oap_dimchange(df: pd.DataFrame):
    df["id"] = df["name"]
    df = fill_columns(df, OAP_DIMCHANGE)
    df = df[OAP_DIMCHANGE]
    return df


def fmt_oap_message(df: pd.DataFrame):
    df["id"] = df["name"]
    df = fill_columns(df, OAP_MESSAGE)
    df = df[OAP_MESSAGE]
    return df


def fmt_oap_propchange(df: pd.DataFrame):
    df["id"] = df["name"]
    df = fill_columns(df, OAP_PROPCHANGE)
    df = df[OAP_PROPCHANGE]
    return df
 

def fmt_oap_propedit(df: pd.DataFrame): 
    df.loc[:, "state_restr"] = col_enum_extract_value(df["state_restr"]) 
    df["id"] = df["name"]
    df = fill_columns(df, OAP_PROPEDIT)
    df = df[OAP_PROPEDIT]
    return df


def fmt_oap_propedit2(df: pd.DataFrame):
    df["id"] = df["name"]
    df = fill_columns(df, OAP_PROPEDIT2)
    df = df[OAP_PROPEDIT2]
    return df


def fmt_oap_text(df: pd.DataFrame):
    if df.empty:
        return df
    assert not df.empty
    df = df.rename(
        {"text_de": "de", "text_en": "en", "text_fr": "fr", "text_nl": "nl"},
        axis=1,
    )

    df = df.melt(
        value_vars=["de", "en", "fr", "nl"],
        var_name="language",
        value_name="text",
        id_vars=["name"],
    )

    df["id"] = df["name"]
    df = fill_columns(df, OAP_TEXT)
    df = df[OAP_TEXT]
    
    # filter language lines without text
    df = df[~df["text"].isna()]

    return df


def fmt_oap_image(df: pd.DataFrame):
    if df.empty:
        return df
    assert not df.empty
    df = df.melt(
        value_vars=[
            "image_xx_dpr1",
            "image_xx_dpr2",
            "image_de_dpr1",
            "image_de_dpr2",
            "image_en_dpr1",
            "image_en_dpr2",
            "image_fr_dpr1",
            "image_fr_dpr2",
            "image_nl_dpr1",
            "image_nl_dpr2",
        ],
        var_name="language",
        value_name="file",
        id_vars=["name"],
    )
    df["language"] = df["language"].str.replace("image_", "")
    df["language"] = df["language"].str.replace("dpr", "")

    language_dpr_df = pd.DataFrame(
        df["language"].str.split("_").to_list(), columns=["language", "dpr"]
    )
    language_dpr_df.loc[language_dpr_df["language"] == "xx", "language"] = ""

    df["language"] = language_dpr_df["language"]
    df["dpr"] = language_dpr_df["dpr"]
    df["id"] = df["name"]

    df = fill_columns(df, OAP_IMAGE)
    df = df[OAP_IMAGE]
    
    # filter language lines without file (but always keep default empty language "")
    df = df[(~df["file"].isna()) | ((df["language"] == "") & (df["dpr"] == 1))]
    return df


def fmt_oap_propeditprops(df: pd.DataFrame):
    df["id"] = df["name"]
    df = fill_columns(df, OAP_PROPEDITPROPS)
    df = df[OAP_PROPEDITPROPS]
    df.loc[:, "state_restr"] = col_enum_extract_value(df["state_restr"])
    return df


def fmt_oap_propeditclasses(df: pd.DataFrame):
    df["id"] = df["name"]
    print("fmt_oap_propeditclasses...", df.columns.to_list())
    df = fill_columns(df, OAP_PROPEDITCLASSES)
    df = df[OAP_PROPEDITCLASSES]
    return df


def fmt_oap_extmedia(df: pd.DataFrame):
    df["id"] = df["name"]
    df = fill_columns(df, OAP_EXTMEDIA)
    df = df[OAP_EXTMEDIA]
    df.loc[:, "type"] = col_enum_extract_value(df["type"])
    return df


def fmt_oap_createobj(df: pd.DataFrame):
    df["id"] = df["name"]
    df = fill_columns(df, OAP_CREATEOBJ)
    df = df[OAP_CREATEOBJ]
    df.loc[:, "art_spec_mode"] = col_enum_extract_value(df["art_spec_mode"])
    df.loc[:, "pos_rot_mode"] = col_enum_extract_value(df["pos_rot_mode"])
    return df


def fmt_oap_action(df: pd.DataFrame):
    df["action"] = df["name"]

    mask_methodcall = df["type"] == ActionType.MethodCall
    mask_createobj = df["type"] == ActionType.CreateObj
    mask_actionchoice = df["type"] == ActionType.ActionChoice
    mask_deleteobj = df["type"] == ActionType.DeleteObj
    mask_dimchange = df["type"] == ActionType.DimChange
    mask_message = df["type"] == ActionType.Message
    mask_noaction = df["type"] == ActionType.NoAction
    mask_propchange = df["type"] == ActionType.PropChange
    mask_propedit = df["type"] == ActionType.PropEdit
    mask_propedit2 = df["type"] == ActionType.PropEdit2
    mask_selectobj = df["type"] == ActionType.SelectObj
    mask_showmedia = df["type"] == ActionType.ShowMedia

    df.loc[mask_methodcall, "parameter"] = df[mask_methodcall]["name_methodcall"]
    df.loc[mask_createobj, "parameter"] = df[mask_createobj]["name_createobj"]
    df.loc[mask_actionchoice, "parameter"] = df[mask_actionchoice]["name_actionchoice"]
    # df.loc[mask_deleteobj, "parameter"] = df[mask_deleteobj]["name_deleteobj"]
    df.loc[mask_dimchange, "parameter"] = df[mask_dimchange]["name_dimchange"]
    df.loc[mask_message, "parameter"] = df[mask_message]["name_message"]
    # df.loc[mask_noaction, "parameter"] = df[mask_noaction]["name_noaction"]
    df.loc[mask_propchange, "parameter"] = df[mask_propchange]["name_propchange"]
    df.loc[mask_propedit, "parameter"] = df[mask_propedit]["name_propedit"]
    df.loc[mask_propedit2, "parameter"] = df[mask_propedit2]["name_propedit2"]
    # df.loc[mask_selectobj, "parameter"] = df[mask_selectobj]["name_selectobj"]
    df.loc[mask_showmedia, "parameter"] = df[mask_showmedia]["name_extmedia"]

    df = fill_columns(df, OAP_ACTION)
    df = df[OAP_ACTION]
    df.loc[:, "type"] = col_enum_extract_value(df["type"])
    return df


def fmt_oap_actionchoice(df: pd.DataFrame):
    df["id"] = df["name"]
    df = fill_columns(df, OAP_ACTIONCHOICE)
    df = df[OAP_ACTIONCHOICE]
    df.loc[:, "view_type"] = col_enum_extract_value(df["view_type"])
    df.loc[:, "argument"] = col_enum_extract_value(df["argument"])
    return df


def fmt_oap_actionlist(df: pd.DataFrame):
    df["id"] = df["name"]
    df["text_id"] = df["text_id_"]
    df["image_id"] = df["image_id_"]
    df = fill_columns(df, OAP_ACTIONLIST)
    df = df[OAP_ACTIONLIST]
    return df


def fmt_oap_numtripel(df: pd.DataFrame):
    df["id"] = df["name"]
    df = fill_columns(df, OAP_NUMTRIPEL)
    df = df[OAP_NUMTRIPEL]
    return df


def fmt_oap_symboldisplay(df: pd.DataFrame):
    df = fill_columns(df, OAP_SYMBOLDISPLAY)
    df = df[OAP_SYMBOLDISPLAY]
    df.loc[:, "offset_type"] = col_enum_extract_value(df["offset_type"])
    return df


def fmt_oap_type(df: pd.DataFrame):
    df["type_id"] = df["name"]
    df = fill_columns(df, OAP_TYPE)
    df = df[OAP_TYPE]
    return df


def fmt_oap_version(df: pd.DataFrame):
    df["format_version"] = df["oap_version"]
    df = fill_columns(df, OAP_VERSION)
    df = df[OAP_VERSION]
    return df
