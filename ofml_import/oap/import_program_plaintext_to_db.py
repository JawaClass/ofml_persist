from collections import defaultdict
from pathlib import Path
from pprint import pprint
import shutil
from typing import Any
import numpy as np
import pandas as pd
from api_models.oap.createobj import OapCreateObjCreate
from models.oap import (
    OapDimChangeDB,
    OapMessageDB,
    OapProgramDB,
    OapMetaType2TypeDB,
    OapArticle2TypeDB,
    OapPropChangeDB,
    OapPropEditDB,
    OapTypeDB,
    OapInteractorDB,
    OapSymbolDisplayDB,
    OapNumTripelDB,
    OapActionDB,
    ActionType,
    OapMethodCallDB,
    OapInteractorActionAssocDB,
    OapExtMediaDB,
    OapActionChoiceDB,
    OapTextDB,
    OapActionListItemDB,
    OapActionListListDB,
    OapActionListActionAssocDB,
    OapImageDB,
    OapPropEdit2DB,
    OapPropEditPropsItemDB,
    OapPropEditPropsListDB,
    OapPropEditClassesListDB,
    OapPropEditClassesItemDB,
    OapCreateObjDB,
    OapObjectDB,
    OffsetType,
    MessageArgType,
    StateRestrType,
)
from sqlalchemy.orm import Session
from ofml_api.repository import OFMLPart, Table
import logging
from ofml_import import util
from ofml_import.text_util import get_language_2_text
import constants

memoize_insert = util.memoize_insert
extract_single_row = util.extract_single_row
extract_single_row2 = util.extract_single_row2
extract_multi_row = util.extract_multi_row
extract_multi_row2 = util.extract_multi_row2
logger = logging.getLogger("inser_oap")


def row_field_or_none(row: pd.Series, field_name: str):
    if field_name in row.index:
        return row[field_name]
    return None


def split_field(string: str):
    return [s.strip() for s in string.split(",")]


def get_language_2_image(df: pd.DataFrame) -> dict[str, str]:
    df.loc[df["language"].isna(), "language"] = "xx"

    def f(df: pd.DataFrame, language: str, dpr: int) -> str:
        result = df[(df["language"] == language) & (df["dpr"] == dpr)]
        return result["file"].iloc[0] if not result.empty else None

    return {
        "de_dpr1": f(df, "de", dpr=1),
        "de_dpr2": f(df, "de", dpr=2),
        "en_dpr1": f(df, "en", dpr=1),
        "en_dpr2": f(df, "en", dpr=2),
        "fr_dpr1": f(df, "fr", dpr=1),
        "fr_dpr2": f(df, "fr", dpr=2),
        "nl_dpr1": f(df, "nl", dpr=1),
        "nl_dpr2": f(df, "nl", dpr=2),
        "xx_dpr1": f(df, "xx", dpr=1),
        "xx_dpr2": f(df, "xx", dpr=2),
    }


class InsertOap:

    def add_unresolved_entry(self, table_name: str, identifier: Any):
        self.unresolved_entries[table_name].append(identifier)

    @memoize_insert("oap_createobj")
    def extract_createobj(self, createobj_id: str) -> OapCreateObjDB:
        row = extract_single_row2(
            "oap_createobj",
            self.oap_createobj.df,
            {"id": createobj_id},
            assert_shape_1=self.assert_references,
        )
        if row is None:
            self.add_unresolved_entry("oap_createobj", createobj_id)
            return None

        ref_parent = self.extract_object(row.parent)

        if ref_parent is None:
            self.add_unresolved_entry("oap_createobj", createobj_id)
            return None

        return OapCreateObjDB(
            name=createobj_id,
            ref_parent=ref_parent,
            art_spec_mode=row.art_spec_mode,
            package=row.package,
            article_id=row.article_id,
            var_code=row.var_code,
            pos_rot_mode=row.pos_rot_mode,
            pos_rot_arg1=row.pos_rot_arg1,
            pos_rot_arg2=row.pos_rot_arg2,
            pos_rot_arg3=row.pos_rot_arg3,
            ref_program=self.program,
        )

    @memoize_insert("oap_object")
    def extract_object(self, object_id: str) -> OapObjectDB:
        row = extract_single_row2(
            "oap_object",
            self.oap_object.df,
            {"id": object_id},
            self.assert_references,
        )

        if row is None:
            self.add_unresolved_entry("oap_object", object_id)
            return None
        
        return OapObjectDB(
            name=object_id,
            category=row.category,
            argument1=row.argument1,
            argument2=row.argument2,
            argument3=row.argument3,
            ref_program=self.program,
        )

    @memoize_insert("oap_image")
    def extract_image(self, image_id: str) -> OapImageDB:
        print("extract_image........", image_id)
        if image_id is None:
            return None

        result = extract_multi_row2(
            "oap_image", self.oap_image.df, {"id": image_id}, self.assert_references
        )

        if result is None:
            self.add_unresolved_entry("oap_image", image_id)
            return None

        images = get_language_2_image(result)
        return OapImageDB(
            name=image_id,
            image_de_dpr1=images["de_dpr1"],
            image_de_dpr2=images["de_dpr2"],
            image_en_dpr1=images["en_dpr1"],
            image_en_dpr2=images["en_dpr2"],
            image_fr_dpr1=images["fr_dpr1"],
            image_fr_dpr2=images["fr_dpr2"],
            image_nl_dpr1=images["nl_dpr1"],
            image_nl_dpr2=images["nl_dpr2"],
            image_xx_dpr1=images["xx_dpr1"],
            image_xx_dpr2=images["xx_dpr2"],
            ref_program=self.program,
        )

    @memoize_insert("oap_propeditprops")
    def extract_propeditprops(self, propeditprops_id: str) -> OapPropEditPropsListDB:
        print("extract_propeditprops... propeditprops_id", propeditprops_id)
        rows = extract_multi_row2(
            "oap_propeditprops",
            self.oap_propeditprops.df,
            {"id": propeditprops_id},
            self.assert_references,
        )

        if rows is None:
            self.add_unresolved_entry("oap_propeditprops", propeditprops_id)
            return None
        
        items = rows.apply(
            lambda row: OapPropEditPropsItemDB(
                property=row.property,
                condition=row.condition,
                state_restr=row.state_restr,
                ref_program=self.program,
            ),
            axis=1,
        ).to_list()

        return OapPropEditPropsListDB(
            name=propeditprops_id, ref_items=items, ref_program=self.program
        )

    @memoize_insert("oap_propeditclasses")
    def extract_propeditclasses(
        self, propeditclasses_id: str
    ) -> OapPropEditClassesListDB: 
        rows = extract_multi_row2(
            "oap_propeditclasses",
            self.oap_propeditclasses.df,
            {"id": propeditclasses_id},
            self.assert_references,
        )

        if rows is None:
            self.add_unresolved_entry("oap_propeditclasses", propeditclasses_id)
            return None
        
        items = rows.apply(
            lambda row: OapPropEditClassesItemDB(
                prop_class=row.prop_class,
                condition=row.condition,
                state_restr=row.state_restr,
                ref_program=self.program,
            ),
            axis=1,
        ).to_list()

        return OapPropEditClassesListDB(name=propeditclasses_id, ref_items=items)

    @memoize_insert("oap_propedit2")
    def extract_propedit2(self, propedit2_id: str) -> OapPropEdit2DB:
        row = extract_single_row2(
            "oap_propedit2",
            self.oap_propedit2.df,
            {"id": propedit2_id},
            self.assert_references,
        )

        if row is None:
            self.add_unresolved_entry("oap_propedit2", propedit2_id)
            return None
        
        return OapPropEdit2DB(
            name=propedit2_id,
            ref_program=self.program,
            ref_title=self.extract_text(row.title),
            ref_propeditprops_list=(
                self.extract_propeditprops(row.properties)
                if row.properties is not None
                else None
            ),
            ref_propeditclasses_list=(
                self.extract_propeditclasses(row.classes)
                if row.classes is not None
                else None
            ),
        )

    @memoize_insert("oap_propedit")
    def extract_propedit(self, propedit_id: str) -> OapPropEditDB:
        row = extract_single_row2(
            "oap_propedit",
            self.oap_propedit.df,
            {"id": propedit_id},
            self.assert_references,
        )

        if row is None:
            self.add_unresolved_entry("oap_propedit", propedit_id)
            return None

        return OapPropEditDB(
            name=propedit_id,
            ref_program=self.program,
            ref_title=self.extract_text(row.title),
            state_restr=row.get("state_restr", StateRestrType.None_),
            properties=row.properties,
            classes=row.classes,
        )

    @memoize_insert("oap_actionchoice")
    def extract_actionchoice(self, actionchoice_id: str) -> OapActionChoiceDB:
        row = extract_single_row2(
            "oap_actionchoice",
            self.oap_actionchoice.df,
            # self.oap_actionchoice.df["id"] == actionchoice_id,
            {"id": actionchoice_id},
            self.assert_references,
        )

        if row is None:
            self.add_unresolved_entry("oap_actionchoice", actionchoice_id)
            return None
        
        return OapActionChoiceDB(
            name=actionchoice_id,
            view_type=row.view_type,
            argument=row.argument,
            ref_program=self.program,
            ref_title=self.extract_text(row.title),
            ref_actionlistlist=OapActionListListDB(
                name=row.list_id,
                ref_actionlist=self.extract_actionlist(row.list_id),
                ref_program=self.program,
            ),
        )

    @memoize_insert("oap_actionlist")
    def extract_actionlist(self, actionlist_id: str) -> list[OapActionListItemDB]:
        result = extract_multi_row2(
            "oap_actionlist",
            self.oap_actionlist.df,
            {"id": actionlist_id},
            assert_not_empty=self.assert_references,
        )
        if result is None:
            self.add_unresolved_entry("oap_actionlist", actionlist_id)
            return []

        return result.apply(
            lambda row: OapActionListItemDB(
                position=row.position,
                condition=row.condition,
                ref_program=self.program,
                ref_text=self.extract_text(row.text_id),
                ref_image=self.extract_image(row.image_id),
                ref_actions=[
                    OapActionListActionAssocDB(
                        # ref_program=self.program,
                        ref_action=self.extract_action(_),
                        position=idx,
                    )
                    for idx, _ in enumerate(split_field(row.actions))
                ],
            ),
            axis=1,
        ).to_list()

    @memoize_insert("oap_text")
    def extract_text(self, text_id: str) -> OapTextDB | None:
        if text_id is None:
            return None
        print("extract_text....", text_id, type(text_id), len(text_id))
        text_df = extract_multi_row2(
            "oap_text", self.oap_text.df, {"id": text_id}, self.assert_references
        )
        if text_df is None:
            self.add_unresolved_entry("oap_text", text_id)
            return None
        language2text = get_language_2_text(text_df, multi=False)
        return OapTextDB(
            name=text_id,
            ref_program=self.program,
            text_de=language2text["de"],
            text_en=language2text["en"],
            text_fr=language2text["fr"],
            text_nl=language2text["nl"],
        )

    @memoize_insert("oap_extmedia")
    def extract_extmedia(self, extmedia_id: str) -> OapExtMediaDB:
        print("extmedia_id", extmedia_id)
        row = extract_single_row2(
            "oap_extmedia",
            self.oap_extmedia.df,
            {"id": extmedia_id},
            self.assert_references,
        )
        if row is None:
            self.add_unresolved_entry("oap_extmedia", extmedia_id)
            return None
        return OapExtMediaDB(
            name=row.id, ref_program=self.program, type=row.type, media=row.media
        )

    @memoize_insert("oap_methodcall")
    def extract_methodcall(self, methodcall_id: str) -> OapMethodCallDB:
        row = extract_single_row2(
            "oap_methodcall",
            self.oap_methodcall.df,
            {"id": methodcall_id},
            assert_shape_1=self.assert_references,
        )
        if row is None:
            self.add_unresolved_entry("oap_methodcall", methodcall_id)
            return None
        return OapMethodCallDB(
            name=row.id,
            ref_program=self.program,
            type=row.type,
            context=row.context,
            method=row.method,
            arguments=row.arguments,
        )

    @memoize_insert("oap_dimchange")
    def extract_dimchange(self, dimchange_id: str) -> OapDimChangeDB:
        row = extract_single_row2(
            "oap_dimchange",
            self.oap_dimchange.df,
            {"id": dimchange_id},
            self.assert_references,
        )
        if row is None:
            self.add_unresolved_entry("oap_dimchange", dimchange_id)
            return None
        return OapDimChangeDB(
            name=row.id,
            ref_program=self.program,
            dimension=row.dimension,
            condition=row.condition,
            separate=row.separate,
            third_dim=row.thirddim,
            property=row.property,
            multiplier=row.multiplier,
            precision=row.precision,
        )

    @memoize_insert("oap_message")
    def extract_message(self, message_id: str) -> OapMessageDB:
        print("extract_message...", message_id)
        row = extract_single_row2(
            "oap_message",
            self.oap_message.df,
            {"id": message_id},
            self.assert_references,
        )
        if row is None:
            self.add_unresolved_entry("oap_message", message_id)
            return None
        oap_message = OapMessageDB(
            name=row.id,
            arg_type=row.arg_type,
            ref_program=self.program,
        )

        match oap_message.arg_type:
            case MessageArgType.Text:
                oap_message.ref_text = self.extract_text(row.argument)
            case MessageArgType.Method:
                oap_message.ref_action = self.extract_action(row.argument)
        return oap_message

    @memoize_insert("oap_propchange")
    def extract_propchange(self, propchange_id: str) -> OapPropChangeDB:
        row = extract_single_row2(
            "oap_propchange",
            self.oap_propchange.df,
            {"id": propchange_id},
            self.assert_references,
        )
        if row is None:
            self.add_unresolved_entry("oap_propchange", propchange_id)
            return None
        return OapPropChangeDB(
            name=row.id,
            type=row.type,
            property=row.property,
            value=row.value,
            ref_program=self.program,
        )

    @memoize_insert("oap_action")
    def extract_action(self, action: str) -> OapActionDB:
        print("extract_action...", action)
        row = extract_single_row2(
            "oap_action",
            self.oap_action.df,
            {"action": action},
            self.assert_references,
        )
        if row is None:
            self.add_unresolved_entry("oap_action", action)
            return None

        oap_action = OapActionDB(
            name=row.action,
            ref_program=self.program,
            condition=row.condition,
            type=row.type,
            ref_objects=(
                [self.extract_object(_) for _ in split_field(row.objects)]
                if row.objects is not None
                else []
            ),
        )

        match oap_action.type:
            case ActionType.MethodCall.value:
                oap_action.ref_methodcall = self.extract_methodcall(row.parameter)
            case ActionType.ShowMedia.value:
                oap_action.ref_extmedia = self.extract_extmedia(row.parameter)
            case ActionType.ActionChoice.value:
                oap_action.ref_actionchoice = self.extract_actionchoice(row.parameter)
            case ActionType.PropEdit2.value:
                oap_action.ref_propedit2 = self.extract_propedit2(row.parameter)
            case ActionType.PropEdit.value:
                oap_action.ref_propedit = self.extract_propedit(row.parameter)
            case ActionType.CreateObj.value:
                oap_action.ref_createobj = self.extract_createobj(row.parameter)
            case ActionType.DimChange.value:
                oap_action.ref_dimchange = self.extract_dimchange(row.parameter)
            case ActionType.Message.value:
                oap_action.ref_message = self.extract_message(row.parameter)
            case ActionType.PropChange.value:
                oap_action.ref_propchange = self.extract_propchange(row.parameter)
            case ActionType.DeleteObj.value:
                pass  # empty field. nothing to extract
            case ActionType.NoAction.value:
                pass  # empty field. nothing to extract
            case ActionType.SelectObj.value:
                pass  # empty field. nothing to extract
            case _:
                raise ValueError(f"ActionType {oap_action.type} not implemented")

        return oap_action

    @memoize_insert("oap_numtripel")
    def extract_numtripel(self, numtripel_id: str) -> OapNumTripelDB:
        print("extract_numtripel...", numtripel_id)

        row = extract_single_row2(
            "oap_numtripel",
            self.oap_numtripel.df,
            {"id": numtripel_id},
            self.assert_references,
        )

        if row is None:
            self.add_unresolved_entry("oap_numtripel", numtripel_id)
            return None

        # NOTE: could validate the x,y,z expressions too
        return OapNumTripelDB(
            name=row.id,
            x=row.x,
            y=row.y,
            z=row.z,
            ref_program=self.program,
        )

    @memoize_insert("oap_symboldisplay")
    def extract_symboldisplay(self, interactor: str) -> list[OapSymbolDisplayDB]:
        print("extract_symboldisplar", interactor)
        assert interactor
        rows = extract_multi_row2(
            "oap_symboldisplay",
            self.oap_symboldisplay.df,
            {"interactor": interactor},
            self.assert_references,
        )

        if rows is None:
            self.add_unresolved_entry("oap_symboldisplay", interactor)
            return []

        return rows.apply(
            lambda row: self.extract_symboldisplay_(row), axis=1
        ).to_list()

    def extract_symboldisplay_(self, row: pd.Series) -> OapSymbolDisplayDB:
        oap_symboldisplay = OapSymbolDisplayDB(
            ref_program=self.program,
            hidden_mode=row_field_or_none(row, "hidden_mode"),
            offset_type=row.get("offset_type", OffsetType.Tripel.value),
            view_angle=row.view_angle,
            ref_direction=(
                self.extract_numtripel(row.direction) if row.direction else None
            ),
            ref_orientation_x=(
                self.extract_numtripel(row.orientation_x) if row.orientation_x else None
            ),
        )

        match oap_symboldisplay.offset_type:
            case OffsetType.Expr.value:
                oap_symboldisplay.offset_expr = row.symbol_offset
            case OffsetType.Tripel.value: 
                oap_symboldisplay.ref_offset = self.extract_numtripel(row.symbol_offset)
            case _:
                raise ValueError(
                    f"OffsetType {oap_symboldisplay.offset_type} not implemented"
                )

        return oap_symboldisplay

    @memoize_insert("oap_interactor")
    def extract_interactor(self, interactor: str) -> OapInteractorDB:
        print("extract_interactor..........", interactor)
        assert interactor
        row = extract_single_row2(
            "oap_interactor",
            self.oap_interactor.df,
            {"interactor": interactor},
            assert_shape_1=self.assert_references,
        )

        if row is None:
            self.add_unresolved_entry("oap_interactor", interactor)
            return None

        return OapInteractorDB(
            name=row.interactor,
            ref_program=self.program,
            condition=row.condition,
            needs_plan_mode=row.get("needs_plan_mode", None),
            symbol_type=row.symbol_type,
            symbol_size=row.symbol_size,
            ref_symboldisplays=self.extract_symboldisplay(interactor),
            ref_actions=[
                OapInteractorActionAssocDB(
                    # ref_program=self.program,
                    ref_action=self.extract_action(_),
                    position=idx,
                )
                for idx, _ in enumerate(split_field(row.actions))
            ],
        )

    @memoize_insert("oap_type")
    def extract_type(self, type_id: str) -> OapTypeDB:
        assert type_id
        print("extract_type......", type_id)
        row = extract_single_row2(
            "oap_type",
            self.oap_type.df,
            {"type_id": type_id},
            self.assert_references,
        )

        if row is None:
            self.add_unresolved_entry("oap_type", type_id)
            return None

        return OapTypeDB(
            name=row.type_id,
            ref_program=self.program,
            general_info=row.general_info,
            prop_change_actions=row.prop_change_actions,
            active_att_areas=row.active_att_areas,
            passive_att_areas=row.passive_att_areas,
            ref_interactor=[
                interactor
                for _ in split_field(row.interactors)
                if (interactor := self.extract_interactor(_)) is not None
            ],
        )

    @memoize_insert("oap_article2type")
    def extract_article2type(
        self, manufacturer_id: str, series_id: str, article_id: str
    ) -> OapArticle2TypeDB:
        assert all([manufacturer_id, series_id, article_id])
        row = extract_single_row2(
            "oap_article2type",
            self.oap_article2type.df,
            {
                "manufacturer_id": manufacturer_id,
                "series_id": series_id,
                "article_id": article_id,
            },
            self.assert_references,
        )

        if row is None:
            self.add_unresolved_entry("oap_article2type", (manufacturer_id, series_id, article_id))
            return None

        return OapArticle2TypeDB(
            manufacturer_id=row.manufacturer_id,
            series_id=row.series_id,
            article_id=row.article_id,
            var_type=row.var_type,
            ref_program=self.program,
            ref_type=self.extract_type(row.type_id),
        )

    @memoize_insert("oap_metatype2type")
    def extract_metatype2type(
        self, manufacturer: str, series: str, metatype_id: str
    ) -> OapMetaType2TypeDB:
        assert all([manufacturer, series, metatype_id])
        row = extract_single_row2(
            "oap_metatype2type",
            self.oap_metatype2type.df,
            {
                "manufacturer": manufacturer,
                "series": series,
                "metatype_id": metatype_id,
            },
            self.assert_references,
        )

        if row is None:
            self.add_unresolved_entry("oap_metatype2type", (manufacturer, series, metatype_id))
            return None
         
        return OapMetaType2TypeDB(
            manufacturer=row.manufacturer,
            series=row.series,
            metatype_id=row.metatype_id,
            var_type=row.get("var_type", None),
            ref_program=self.program,
            ref_type=self.extract_type(row.type_id),
        )

    def copy_image(self, image: OapImageDB, dst_images_folder: Path):
        oap_path = self.oap.path
        for img_path in [
            image.image_de_dpr1,
            image.image_de_dpr2,
            image.image_en_dpr1,
            image.image_en_dpr2,
            image.image_fr_dpr1,
            image.image_fr_dpr2,
            image.image_nl_dpr1,
            image.image_nl_dpr2,
            image.image_xx_dpr1,
            image.image_xx_dpr2,
        ]:
            if img_path:

                src_abs_path = oap_path / img_path

                if not src_abs_path.exists():
                    logger.warning(f"Source Image Path does not exist: {src_abs_path}")
                    continue

                dst_abs_path = dst_images_folder / img_path

                if not dst_abs_path.parent.exists():
                    dst_abs_path.parent.mkdir(parents=True)

                shutil.copyfile(src_abs_path, dst_abs_path)

    def copy_images(self):
        id2image: dict[str, OapImageDB] = self.identy_map_by_key.get("oap_image")

        if not id2image:
            return

        dst_images_folder = (
            constants.root_path / "resources/oap/images" / self.program.name
        )
        if not dst_images_folder.exists():
            dst_images_folder.mkdir()
        for img in id2image.values():
            if img is not None:
                self.copy_image(img, dst_images_folder)

    def __init__(
        self,
        oap: OFMLPart,
        session: Session,
        program_name: str,
        description: str | None = None,
        assert_references: bool = False,
    ):
        self.assert_references = assert_references
        self.identy_map_by_key = defaultdict(dict)
        self.oap = oap

        self.unresolved_entries = defaultdict(list)

        def oap_table(name: str):
            return oap.table(name) if name.replace(".csv", "") in oap.tables else None

        self.oap_version = oap_table("oap_version.csv")
        self.oap_metatype2type = oap.table("oap_metatype2type.csv")
        self.oap_article2type = oap.table("oap_article2type.csv")
        self.oap_type = oap.table("oap_type.csv")
        self.oap_interactor = oap.table("oap_interactor.csv")
        self.oap_symboldisplay = oap.table("oap_symboldisplay.csv")
        self.oap_numtripel = oap.table("oap_numtripel.csv")
        self.oap_action = oap.table("oap_action.csv")
        self.oap_methodcall = oap.table("oap_methodcall.csv")
        self.oap_extmedia = oap_table("oap_extmedia.csv")
        self.oap_actionchoice = oap.table("oap_actionchoice.csv")
        self.oap_text = oap.table("oap_text.csv")
        self.oap_actionlist = oap.table("oap_actionlist.csv")
        self.oap_propedit2 = oap_table("oap_propedit2.csv")
        self.oap_propedit = oap_table("oap_propedit.csv")
        self.oap_createobj = oap.table("oap_createobj.csv")
        self.oap_object = oap.table("oap_object.csv")
        self.oap_image = oap.table("oap_image.csv")
        self.oap_propeditprops = oap_table("oap_propeditprops.csv")
        self.oap_propeditclasses = oap_table("oap_propeditclasses.csv")
        self.oap_dimchange = oap_table("oap_dimchange.csv")
        self.oap_message = oap_table("oap_message.csv")
        self.oap_propchange = oap_table("oap_propchange.csv")

        version_string = (
            self.oap_version.df.iloc[0, 0]
            if isinstance(self.oap_version, Table)
            else ""
        )

        self.program = OapProgramDB(
            name=program_name,
            import_path=str(oap.path),
            oap_version=version_string,
            description=description,
        )


def ofml2dbscheme(
    oap: OFMLPart,
    session: Session,
    program_name: str,
    description: str | None = None,
):
    return InsertOap(oap, session, program_name, description)
