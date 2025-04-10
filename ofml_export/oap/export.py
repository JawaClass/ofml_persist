import csv
from pathlib import Path
from models import engine, get_engine

import shutil
from models.oap import (
    ActionType,
    OapActionChoiceDB,
    OapActionDB,
    OapActionListActionAssocDB,
    OapActionListItemDB,
    OapActionListListDB,
    OapInteractorActionAssocDB,
    OapInteractorDB,
    OapArticle2TypeDB,
    OapMetaType2TypeDB,
    OapObjectDB,
    OapMethodCallDB,
    OapDimChangeDB,
    OapMessageDB,
    OapPropChangeDB,
    OapPropEdit2DB,
    OapPropEditClassesListDB,
    OapPropEditDB,
    OapPropEditPropsListDB,
    OapTextDB,
    OapImageDB,
    OapPropEditPropsItemDB,
    OapPropEditClassesItemDB,
    OapExtMediaDB,
    OapCreateObjDB,
    OapNumTripelDB,
    OapSymbolDisplayDB,
    OapTypeDB,
    OapProgramDB,
)
from ofml_export.base.export import ExportBase
import ofml_export.oap.formatting as formatter
from sqlalchemy import case, func, select, text
from sqlalchemy.orm import Session, aliased
from ofml_export.oap.inp_descr.version_1_6 import INP_DESCR
from ofml_export.util import as_path

OAP_MAKER_EXPORT_FLAG_FILE_NAME = ".oap_maker_export"

class OapExport(ExportBase):

    def __init__(self, program_name: str, engine, export_path: Path | str) -> None:
        super().__init__(program_name, engine)
        self.export_path = as_path(export_path)
        self.programdb = self.session.execute(
            select(OapProgramDB).where(OapProgramDB.name == program_name)
        ).scalar_one()
        print("OapExport", self.program_name)
        print("programdb:", self.programdb)

    def extract_version(self):
        df = self.read_sql(
            self.session.query(
                OapProgramDB,
            )
            .where(OapProgramDB.id == self.programdb.id)
            .statement
        )
        df["oap_version"] = "1.6"
        return df

    def extract_type(self):
        df = self.read_sql(
            self.session.query(
                OapTypeDB,
                func.group_concat(OapInteractorDB.name, ",").label("interactors"),
            )
            .outerjoin(OapInteractorDB, OapTypeDB.ref_interactor)
            .group_by(OapTypeDB.id)
            .where(OapTypeDB.program_id == self.programdb.id)
            .statement
        )
        return df

    def extract_symboldisplay(self):
        direction_alias = aliased(OapNumTripelDB)
        offset_alias = aliased(OapNumTripelDB)
        orientation_alias = aliased(OapNumTripelDB)

        df = self.read_sql(
            self.session.query(
                OapSymbolDisplayDB,
                OapInteractorDB.name.label("interactor"),
                direction_alias.name.label("direction"),
                offset_alias.name.label("symbol_offset"),
                orientation_alias.name.label("orientation_x"),
            )
            .join(
                OapInteractorDB, OapSymbolDisplayDB.interactor_id == OapInteractorDB.id
            )
            .outerjoin(
                direction_alias, OapSymbolDisplayDB.direction_id == direction_alias.id
            )
            .outerjoin(offset_alias, OapSymbolDisplayDB.offset_id == offset_alias.id)
            .outerjoin(
                orientation_alias,
                OapSymbolDisplayDB.orientation_x_id == orientation_alias.id,
            )
            .where(OapSymbolDisplayDB.program_id == self.programdb.id)
            .statement
        )
        return df

    def extract_numtripel(self):
        df = self.read_sql(
            self.session.query(OapNumTripelDB)
            .where(OapNumTripelDB.program_id == self.programdb.id)
            .statement
        )
        return df

    def extract_actionlist(self):
        df = self.read_sql(
            self.session.query(
                OapActionListItemDB,
                OapActionListListDB.name.label("name"),
                OapImageDB.name.label("image_id_"),
                OapTextDB.name.label("text_id_"),
                func.group_concat(OapActionDB.name, ",").label("actions"),
            )
            .join(
                OapActionListListDB,
                OapActionListListDB.id == OapActionListItemDB.actionlistlist_id,
            )
            .outerjoin(OapImageDB, OapActionListItemDB.ref_image)
            .outerjoin(OapTextDB, OapActionListItemDB.ref_text)
            .outerjoin(OapActionListActionAssocDB, OapActionListItemDB.ref_actions)
            .outerjoin(
                OapActionDB, OapActionDB.id == OapActionListActionAssocDB.action_id
            )
            .group_by(OapActionListItemDB.id)
            .order_by(OapActionListItemDB.id, OapActionListActionAssocDB.position)
            .where(OapActionListItemDB.program_id == self.programdb.id)
            .statement
        )
        return df

    def extract_actionchoice(self):
        df = self.read_sql(
            self.session.query(
                OapActionChoiceDB,
                OapTextDB.name.label("title"),
                OapActionListListDB.name.label("list_id"),
            )
            .outerjoin(OapTextDB, OapActionChoiceDB.ref_title)
            .outerjoin(OapActionListListDB, OapActionChoiceDB.ref_actionlistlist)
            .where(OapActionChoiceDB.program_id == self.programdb.id)
            .statement
        )
        return df

    def extract_action(self):

        query = self.session.query(
            OapActionDB,
            OapMessageDB.name.label("name_message"),
            OapDimChangeDB.name.label("name_dimchange"),
            OapPropChangeDB.name.label("name_propchange"),
            OapPropEditDB.name.label("name_propedit"),
            OapPropEdit2DB.name.label("name_propedit2"),
            OapExtMediaDB.name.label("name_extmedia"),
            OapCreateObjDB.name.label("name_createobj"),
            OapMethodCallDB.name.label("name_methodcall"),
            OapActionChoiceDB.name.label("name_actionchoice"),
            func.group_concat(OapObjectDB.name, ",").label("objects"),
        )

        query = (
            (
                query.outerjoin(
                    OapMessageDB,
                    case(
                        (
                            OapActionDB.type == ActionType.Message,
                            OapActionDB.message_id == OapMessageDB.id,
                        ),
                        else_=False,
                    ),
                )
                .outerjoin(
                    OapDimChangeDB,
                    case(
                        (
                            OapActionDB.type == ActionType.DimChange,
                            OapActionDB.dimchange_id == OapDimChangeDB.id,
                        ),
                        else_=False,
                    ),
                )
                .outerjoin(
                    OapPropChangeDB,
                    case(
                        (
                            OapActionDB.type == ActionType.PropChange,
                            OapActionDB.propchange_id == OapPropChangeDB.id,
                        ),
                        else_=False,
                    ),
                )
                .outerjoin(
                    OapPropEditDB,
                    case(
                        (
                            OapActionDB.type == ActionType.PropEdit,
                            OapActionDB.propedit_id == OapPropEditDB.id,
                        ),
                        else_=False,
                    ),
                )
                .outerjoin(
                    OapPropEdit2DB,
                    case(
                        (
                            OapActionDB.type == ActionType.PropEdit2,
                            OapActionDB.propedit2_id == OapPropEdit2DB.id,
                        ),
                        else_=False,
                    ),
                )
                .outerjoin(
                    OapExtMediaDB,
                    case(
                        (
                            OapActionDB.type == ActionType.ShowMedia,
                            OapActionDB.extmedia_id == OapExtMediaDB.id,
                        ),
                        else_=False,
                    ),
                )
                .outerjoin(
                    OapCreateObjDB,
                    case(
                        (
                            OapActionDB.type == ActionType.CreateObj,
                            OapActionDB.createobj_id == OapCreateObjDB.id,
                        ),
                        else_=False,
                    ),
                )
                .outerjoin(
                    OapMethodCallDB,
                    case(
                        (
                            OapActionDB.type == ActionType.MethodCall,
                            OapActionDB.methodcall_id == OapMethodCallDB.id,
                        ),
                        else_=False,
                    ),
                )
                .outerjoin(
                    OapActionChoiceDB,
                    case(
                        (
                            OapActionDB.type == ActionType.ActionChoice,
                            OapActionDB.actionchoice_id == OapActionChoiceDB.id,
                        ),
                        else_=False,
                    ),
                )
            )
            .outerjoin(OapObjectDB, OapActionDB.ref_objects)
            .group_by(OapActionDB.id)
        ).where(OapActionDB.program_id == self.programdb.id)

        print("read_action_query.....")
        print(query.statement)

        df = self.read_sql(query.statement)
        print("result size", df.shape)
        return df

    def extract_createobj(self):
        df = self.read_sql(
            self.session.query(
                OapCreateObjDB,
                OapObjectDB.name.label("parent"),
            )
            .outerjoin(OapObjectDB)
            .where(OapCreateObjDB.program_id == self.programdb.id)
            .statement
        )
        return df

    def extract_extmedia(self):
        df = self.read_sql(
            self.session.query(OapExtMediaDB)
            .where(OapExtMediaDB.program_id == self.programdb.id)
            .statement
        )
        return df

    def extract_propeditclasses(self):

        df = self.read_sql(
            self.session.query(
                OapPropEditClassesItemDB, OapPropEditClassesListDB.name.label("name")
            )
            .join(OapPropEditClassesListDB)
            .where(OapPropEditClassesItemDB.program_id == self.programdb.id)
            .statement
        )
        return df

    def extract_propeditprops(self):

        df = self.read_sql(
            self.session.query(
                OapPropEditPropsItemDB, OapPropEditPropsListDB.name.label("name")
            )
            .join(OapPropEditPropsListDB)
            .where(OapPropEditPropsItemDB.program_id == self.programdb.id)
            .statement
        )
        return df

    def extract_image(self):
        df = self.read_sql(
            self.session.query(OapImageDB)
            .where(OapImageDB.program_id == self.programdb.id)
            .statement
        )
        print("extract_image....", df.shape)
        return df

    def extract_text(self):
        df = self.read_sql(
            self.session.query(OapTextDB)
            .where(OapTextDB.program_id == self.programdb.id)
            .statement
        )
        return df

    def extract_propedit2(self):
        df = self.read_sql(
            self.session.query(
                OapPropEdit2DB,
                OapTextDB.name.label("title"),
                OapPropEditPropsListDB.name.label("properties"),
                OapPropEditClassesListDB.name.label("classes"),
            )
            .outerjoin(
                OapTextDB,
                OapPropEdit2DB.title_id == OapTextDB.id,
            )
            .outerjoin(
                OapPropEditPropsListDB,
                OapPropEdit2DB.propeditprops_list_id == OapPropEditPropsListDB.id,
            )
            .outerjoin(
                OapPropEditClassesListDB,
                OapPropEdit2DB.propeditclasses_list_id == OapPropEditClassesListDB.id,
            )
            .where(OapPropEdit2DB.program_id == self.programdb.id)
            .statement
        )
        return df

    def extract_propedit(self):
        df = self.read_sql(
            self.session.query(OapPropEditDB, OapTextDB.name.label("title"))
            .outerjoin(OapTextDB, OapPropEditDB.title_id == OapTextDB.id)
            .where(OapPropEditDB.program_id == self.programdb.id)
            .statement
        )
        return df

    def extract_propchange(self):
        df = self.read_sql(
            self.session.query(OapPropChangeDB)
            .where(OapPropChangeDB.program_id == self.programdb.id)
            .statement
        )
        return df

    def extract_message(self):
        df = self.read_sql(
            self.session.query(OapMessageDB)
            .where(OapMessageDB.program_id == self.programdb.id)
            .statement
        )
        return df

    def extract_dimchange(self):
        df = self.read_sql(
            self.session.query(OapDimChangeDB)
            .where(OapDimChangeDB.program_id == self.programdb.id)
            .statement
        )
        return df

    def extract_methodcall(self):
        df = self.read_sql(
            self.session.query(OapMethodCallDB)
            .where(OapMethodCallDB.program_id == self.programdb.id)
            .statement
        )
        return df

    def extract_object(self):
        df = self.read_sql(
            self.session.query(OapObjectDB)
            .where(OapObjectDB.program_id == self.programdb.id)
            .statement
        )
        return df

    def extract_article2type(self):
        df = self.read_sql(
            self.session.query(OapArticle2TypeDB, OapTypeDB.name)
            .outerjoin(OapTypeDB, OapTypeDB.id == OapArticle2TypeDB.type_id)
            .where(OapArticle2TypeDB.program_id == self.programdb.id)
            .statement
        )
        return df

    def extract_metatype2type(self):
        df = self.read_sql(
            self.session.query(OapMetaType2TypeDB, OapTypeDB.name)
            .outerjoin(OapTypeDB, OapTypeDB.id == OapMetaType2TypeDB.type_id)
            .where(OapMetaType2TypeDB.program_id == self.programdb.id)
            .statement
        )

        print("extract_metatype2type....DF", df.shape, "progream_id", self.programdb.id)

        return df

    def extract_interactor(self):
        df = self.read_sql(
            self.session.query(
                OapInteractorDB,
                func.group_concat(OapActionDB.name, ",").label("actions"),
            )
            .outerjoin(
                OapInteractorActionAssocDB,
                OapInteractorDB.id == OapInteractorActionAssocDB.interactor_id,
            )
            .outerjoin(
                OapActionDB,
                OapInteractorActionAssocDB.action_id == OapActionDB.id,
            )
            .group_by(OapInteractorDB.id)
            .order_by(OapInteractorDB.id, OapInteractorActionAssocDB.position)
            .where(OapInteractorDB.program_id == self.programdb.id)
            .statement
        )
        return df

    def extract(self):
        self.tables["interactor"] = self.extract_interactor()
        self.tables["article2type"] = self.extract_article2type()
        self.tables["metatype2type"] = self.extract_metatype2type()
        self.tables["object"] = self.extract_object()
        self.tables["methodcall"] = self.extract_methodcall()
        self.tables["dimchange"] = self.extract_dimchange()
        self.tables["message"] = self.extract_message()
        self.tables["propchange"] = self.extract_propchange()
        self.tables["propedit"] = self.extract_propedit()
        self.tables["propedit2"] = self.extract_propedit2()
        self.tables["text"] = self.extract_text()
        self.tables["image"] = self.extract_image()
        self.tables["propeditprops"] = self.extract_propeditprops()
        self.tables["propeditclasses"] = self.extract_propeditclasses()
        self.tables["extmedia"] = self.extract_extmedia()
        self.tables["createobj"] = self.extract_createobj()
        self.tables["action"] = self.extract_action()
        self.tables["actionchoice"] = self.extract_actionchoice()
        self.tables["actionlist"] = self.extract_actionlist()
        self.tables["numtripel"] = self.extract_numtripel()
        self.tables["symboldisplay"] = self.extract_symboldisplay()
        self.tables["type"] = self.extract_type()
        self.tables["version"] = self.extract_version()
        return self

    def format(self):
        self.tables["interactor"] = formatter.fmt_oap_interactor(
            self.tables["interactor"]
        )
        self.tables["article2type"] = formatter.fmt_oap_article2type(
            self.tables["article2type"]
        )
        self.tables["metatype2type"] = formatter.fmt_oap_metatype2type(
            self.tables["metatype2type"]
        )
        self.tables["object"] = formatter.fmt_oap_object(self.tables["object"])
        self.tables["methodcall"] = formatter.fmt_oap_methodcall(
            self.tables["methodcall"]
        )
        self.tables["dimchange"] = formatter.fmt_oap_dimchange(self.tables["dimchange"])
        self.tables["message"] = formatter.fmt_oap_message(self.tables["message"])
        self.tables["propchange"] = formatter.fmt_oap_propchange(
            self.tables["propchange"]
        )
        self.tables["propedit"] = formatter.fmt_oap_propedit(self.tables["propedit"])
        self.tables["propedit2"] = formatter.fmt_oap_propedit2(self.tables["propedit2"])
        self.tables["text"] = formatter.fmt_oap_text(self.tables["text"])
        self.tables["image"] = formatter.fmt_oap_image(self.tables["image"])
        print("formatted images...", self.tables["image"].shape)
         
        self.tables["propeditprops"] = formatter.fmt_oap_propeditprops(
            self.tables["propeditprops"]
        )
        self.tables["propeditclasses"] = formatter.fmt_oap_propeditclasses(
            self.tables["propeditclasses"]
        )
        self.tables["extmedia"] = formatter.fmt_oap_extmedia(self.tables["extmedia"])
        self.tables["createobj"] = formatter.fmt_oap_createobj(self.tables["createobj"])
        self.tables["action"] = formatter.fmt_oap_action(self.tables["action"])
        self.tables["actionchoice"] = formatter.fmt_oap_actionchoice(
            self.tables["actionchoice"]
        )
        self.tables["actionlist"] = formatter.fmt_oap_actionlist(
            self.tables["actionlist"]
        )
        self.tables["numtripel"] = formatter.fmt_oap_numtripel(self.tables["numtripel"])
        self.tables["symboldisplay"] = formatter.fmt_oap_symboldisplay(
            self.tables["symboldisplay"]
        )
        self.tables["type"] = formatter.fmt_oap_type(self.tables["type"])
        self.tables["version"] = formatter.fmt_oap_version(self.tables["version"])
 
        return self

    def export(self):
        directory = self.export_path
        print("export.directory.exists()", directory.exists())
        if not directory.exists():
            directory.mkdir(parents=True)
 
        for name, df in self.tables.items():
            fname = f"oap_{name}.csv"
            df.to_csv(directory / fname, header=False, sep=";", index=False, quoting=csv.QUOTE_NONE)

        with open(directory / "oap.inp_descr", "w+") as f:
            f.write(INP_DESCR)

        self.build_ebase(directory)

        with open(directory / OAP_MAKER_EXPORT_FLAG_FILE_NAME, "w+") as f:
            from datetime import datetime
            f.write(f"""Export von OAP Maker {datetime.now().strftime('%d/%m/%Y, %H:%M:%S')}
            Wenn diese Datei im oap Ordner existiert, exportiert der OapMaker direkt in oap und überschreibt den alten Stand. 
            """)

        return self

    def export_images(self):
        from constants import root_path

        img_folder = root_path / "resources/oap/images" / self.program_name

        img_folder_exists = img_folder.exists()
        if not img_folder_exists:
            return self
        
        assert img_folder_exists, f"IMG_FOLDER {img_folder} does not exist"
        dst_image_folder = as_path(self.export_path)
        print("copy")
        print("from:", img_folder)
        print("to:", dst_image_folder)
        shutil.copytree(img_folder, dst_image_folder, dirs_exist_ok=True)
        return self

    def build_ebase(self, directory: Path):
        from ofml_export.build_ebase import execute_build_ebase_command
        from constants import root_path

        directory = as_path(directory)
        inp_descr = directory / "oap.inp_descr"
        oap_ebase = directory / "oap.ebase"
        assert directory.exists(), f"oap folder {directory} does not exist"
        assert inp_descr.exists(), f"oap.inp_descr {inp_descr} does not exist"
        ebase_exe = root_path / "tools" / "linux" / "ebmkdb"
        command = f"{ebase_exe} -d {directory} {inp_descr} {oap_ebase}"
        print(command)
        execute_build_ebase_command(command=command)


def export(program: str, engine, export_path: str|None=None):

    if not export_path:
        export_path = f"/mnt/knps_testumgebung/Testumgebung/EasternGraphics/kn/{program}/DE/2/oap_[export]"
        export_flag_file = as_path(export_path) / OAP_MAKER_EXPORT_FLAG_FILE_NAME
        if export_flag_file.exists():
            export_path = f"/mnt/knps_testumgebung/Testumgebung/EasternGraphics/kn/{program}/DE/2/oap"

    exporter = OapExport(engine=engine, program_name=program, export_path=export_path)
        
    exporter.extract()
    
    exporter.format()

    exporter.export()

    if not exporter.tables["image"].empty:
        exporter.export_images()

    return export_path

if __name__ == "__main__":
    export("screens", get_engine(), "oapExportPath")
