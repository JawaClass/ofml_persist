from sqlalchemy import (
    Enum,
    ForeignKey,
    SmallInteger,
    UniqueConstraint,
    DateTime,
    Text,
    String,
    VARCHAR,
    func,
)
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import Column
from sqlalchemy import Table
from sqlalchemy import ForeignKey
from models.base import SqlAlchemyBase
import enum

IDX_STRING_LENGTH = 255
STRING_LENGTH = 1_000
BIG_STRING_LENGTH = 10_000
 
class OapProgramDB(SqlAlchemyBase):
    __tablename__ = "oap_program"
    __table_args__ = (UniqueConstraint("name"),)
    # keys
    id: Mapped[int] = mapped_column(primary_key=True)
    # scalars
    name: Mapped[str] = mapped_column(String(IDX_STRING_LENGTH))
    import_path: Mapped[str] = mapped_column(String(STRING_LENGTH))
    create_date: Mapped[str] = mapped_column(DateTime, server_default=func.now())
    oap_version: Mapped[str] = mapped_column(String(STRING_LENGTH))
    description: Mapped[str | None] = mapped_column(String(BIG_STRING_LENGTH))
    deleted: Mapped[bool] = mapped_column(SmallInteger, default=False)


class ObjectCategory(enum.Enum):
    Self = "Self"
    ParentArticle = "ParentArticle"
    TopArticle = "TopArticle"
    MethodCall = "MethodCall"


class MethodCallType(enum.Enum):
    Instance = "Instance"
    Class = "Class"


class OffsetType(enum.Enum):
    Tripel = "Tripel"
    Expr = "Expr"


class ActionType(enum.Enum):
    ActionChoice = "ActionChoice"
    CreateObj = "CreateObj"
    DeleteObj = "DeleteObj"
    DimChange = "DimChange"
    Message = "Message"
    MethodCall = "MethodCall"
    NoAction = "NoAction"
    PropChange = "PropChange"
    PropEdit2 = "PropEdit2"
    PropEdit = "PropEdit"
    SelectObj = "SelectObj"
    ShowMedia = "ShowMedia"


class MessageArgType(enum.Enum):
    Text = "Text"
    Method = "Method"


class SymbolSize(enum.Enum):
    small = "small"
    medium = "medium"
    large = "large"


class SymbolType(enum.Enum):
    Add = "Add"
    Attention = "Attention"
    ChangeDimHorizontal = "ChangeDimHorizontal"
    ChangeDim2Left = "ChangeDim2Left"
    ChangeDim2Right = "ChangeDim2Right"
    ChangeDimVertical = "ChangeDimVertical"
    ChangeDimDown = "ChangeDimDown"
    ChangeDimUp = "ChangeDimUp"
    Delete = "Delete"
    Edit = "Edit"
    Electrification = "Electrification"
    Flip = "Flip"
    Lighting = "Lighting"
    Material = "Material"
    OnOff = "OnOff"
    PosHorizontal = "PosHorizontal"
    Pos2Left = "Pos2Left"
    Pos2Right = "Pos2Right"
    PosVertical = "PosVertical"
    PosDown = "PosDown"
    PosUp = "PosUp"
    RotateNY = "RotateNY"
    RotateNY90 = "RotateNY90"
    RotatePY = "RotatePY"
    RotatePY90 = "RotatePY90"
    StartDimChange = "StartDimChange"
    Video = "Video"


class PropChangeType(enum.Enum):
    Value = "Value"
    Visibility = "Visibility"
    Editability = "Editability"


class DimChangeDimension(enum.Enum):
    X = "X"
    Y = "Y"
    Z = "Z"
    PX = "PX"
    PY = "PY"
    PZ = "PZ"
    NX = "NX"
    NY = "NY"
    NZ = "NZ"


class ExtMediaType(enum.Enum):
    PIM = "PIM"
    YouTube = "YouTube"


class ArtSpecMode(enum.Enum):
    Explicit = "Explicit"
    Self = "Self"


class PosRotMode(enum.Enum):
    DataDefined = "DataDefined"


class StateRestrType(enum.Enum):
    None_ = "None"
    Visible = "Visible"
    VisibleEditable = "VisibleEditable"


class ActionChoiceViewType(enum.Enum):
    List = "List"
    Tile = "Tile"


class ActionChoiceTileSize(enum.Enum):
    small = "small"
    medium = "medium"
    large = "large"


oap_action_object_association_table = Table(
    "oap_action_object_association_table",
    SqlAlchemyBase.metadata,
    Column("oap_action_id", ForeignKey("oap_action.id", ondelete="CASCADE"), primary_key=True),
    Column("oap_object_id", ForeignKey("oap_object.id", ondelete="CASCADE"), primary_key=True),
)


class OapObjectDB(SqlAlchemyBase):
    __tablename__ = "oap_object"
    __table_args__ = (UniqueConstraint("name", "program_id"),)
    # keys
    id: Mapped[int] = mapped_column(primary_key=True)
    program_id: Mapped[int] = mapped_column(
        ForeignKey("oap_program.id", ondelete="CASCADE")
    )
    # scalars
    name: Mapped[str] = mapped_column(String(IDX_STRING_LENGTH))
    category: Mapped[ObjectCategory] = mapped_column(Enum(ObjectCategory))
    argument1: Mapped[str | None] = mapped_column(String(STRING_LENGTH))
    argument2: Mapped[str | None] = mapped_column(String(STRING_LENGTH))
    argument3: Mapped[str | None] = mapped_column(String(STRING_LENGTH))
    # refs
    ref_program: Mapped[OapProgramDB] = relationship()


class OapCreateObjDB(SqlAlchemyBase):
    __tablename__ = "oap_createobj"
    __table_args__ = (UniqueConstraint("name", "program_id"),)
    # keys
    id: Mapped[int] = mapped_column(primary_key=True)
    program_id: Mapped[int] = mapped_column(
        ForeignKey("oap_program.id", ondelete="CASCADE")
    )
    # scalars
    name: Mapped[str] = mapped_column(String(IDX_STRING_LENGTH))
    parent_id: Mapped[int | None] = mapped_column(ForeignKey("oap_object.id"))
    art_spec_mode: Mapped[ArtSpecMode] = mapped_column(Enum(ArtSpecMode))
    package: Mapped[str] = mapped_column(String(STRING_LENGTH))
    article_id: Mapped[str] = mapped_column(String(STRING_LENGTH))
    var_code: Mapped[str | None] = mapped_column(String(BIG_STRING_LENGTH))
    pos_rot_mode: Mapped[PosRotMode] = mapped_column(Enum(PosRotMode))
    pos_rot_arg1: Mapped[str] = mapped_column(String(STRING_LENGTH))
    pos_rot_arg2: Mapped[str] = mapped_column(String(STRING_LENGTH))
    pos_rot_arg3: Mapped[str | None] = mapped_column(String(STRING_LENGTH))
    # refs
    ref_parent: Mapped[OapObjectDB | None] = relationship()
    ref_program: Mapped[OapProgramDB] = relationship()


class OapExtMediaDB(SqlAlchemyBase):
    __tablename__ = "oap_extmedia"
    __table_args__ = (UniqueConstraint("name", "program_id"),)
    # keys
    id: Mapped[int] = mapped_column(primary_key=True)
    program_id: Mapped[int] = mapped_column(
        ForeignKey("oap_program.id", ondelete="CASCADE")
    )
    # scalars
    name: Mapped[str] = mapped_column(String(IDX_STRING_LENGTH))
    type: Mapped[ExtMediaType] = mapped_column(Enum(ExtMediaType))
    media: Mapped[str] = mapped_column(String(STRING_LENGTH))
    # refs
    ref_program: Mapped[OapProgramDB] = relationship()


class OapPropEditClassesListDB(SqlAlchemyBase):
    __tablename__ = "oap_propeditclasses_list"
    __table_args__ = (UniqueConstraint("name", "program_id"),)
    # keys
    id: Mapped[int] = mapped_column(primary_key=True)
    program_id: Mapped[int] = mapped_column(
        ForeignKey("oap_program.id", ondelete="CASCADE")
    )
    name: Mapped[str] = mapped_column(String(IDX_STRING_LENGTH))
    # refs
    ref_items: Mapped[list["OapPropEditClassesItemDB"]] = relationship(
        order_by="OapPropEditClassesItemDB.id"
    )
    ref_program: Mapped[OapProgramDB] = relationship()


class OapPropEditClassesItemDB(SqlAlchemyBase):
    __tablename__ = "oap_propeditclasses_item"
    __table_args__ = (UniqueConstraint("list_id", "prop_class", "program_id"),)
    # keys
    id: Mapped[int] = mapped_column(primary_key=True)
    program_id: Mapped[int] = mapped_column(
        ForeignKey("oap_program.id", ondelete="CASCADE")
    )
    list_id: Mapped[int | None] = mapped_column(
        ForeignKey("oap_propeditclasses_list.id")
    )
    prop_class: Mapped[str] = mapped_column(String(IDX_STRING_LENGTH))
    condition: Mapped[str | None] = mapped_column(Text)
    state_restr: Mapped[StateRestrType] = mapped_column(
        Enum(
            StateRestrType,
            values_callable=lambda obj: [
                e.value for e in obj
            ],  # Use the enum values in the DB
        )
    )
    ref_program: Mapped[OapProgramDB] = relationship()


class OapPropEditPropsListDB(SqlAlchemyBase):
    __tablename__ = "oap_propeditprops_list"
    __table_args__ = (UniqueConstraint("name", "program_id"),)
    # keys
    id: Mapped[int] = mapped_column(primary_key=True)
    program_id: Mapped[int] = mapped_column(
        ForeignKey("oap_program.id", ondelete="CASCADE")
    )
    # scalar
    name: Mapped[str] = mapped_column(String(IDX_STRING_LENGTH))
    # refs
    ref_items: Mapped[list["OapPropEditPropsItemDB"]] = relationship(
        order_by="OapPropEditPropsItemDB.id"
    )
    ref_program: Mapped[OapProgramDB] = relationship()


class OapPropEditPropsItemDB(SqlAlchemyBase):
    __tablename__ = "oap_propeditprops_item"
    __table_args__ = (UniqueConstraint("list_id", "property", "program_id"),)
    # keys
    id: Mapped[int] = mapped_column(primary_key=True)
    program_id: Mapped[int] = mapped_column(
        ForeignKey("oap_program.id", ondelete="CASCADE")
    )
    list_id: Mapped[int] = mapped_column(ForeignKey("oap_propeditprops_list.id"))
    property: Mapped[str] = mapped_column(String(IDX_STRING_LENGTH))
    condition: Mapped[str | None] = mapped_column(Text)
    state_restr: Mapped[StateRestrType] = mapped_column(
        Enum(
            StateRestrType,
            values_callable=lambda obj: [
                e.value for e in obj
            ],  # Use the enum values in the DB
        )
    )
    ref_program: Mapped[OapProgramDB] = relationship()


class OapPropEdit2DB(SqlAlchemyBase):
    __tablename__ = "oap_propedit2"
    __table_args__ = (UniqueConstraint("name", "program_id"),)
    # keys
    id: Mapped[int] = mapped_column(primary_key=True)
    program_id: Mapped[int] = mapped_column(
        ForeignKey("oap_program.id", ondelete="CASCADE")
    )
    name: Mapped[str] = mapped_column(String(IDX_STRING_LENGTH))
    title_id: Mapped[int | None] = mapped_column(ForeignKey("oap_text.id"))
    # only one of those may be None
    propeditprops_list_id: Mapped[int | None] = mapped_column(
        ForeignKey("oap_propeditprops_list.id")
    )
    propeditclasses_list_id: Mapped[int | None] = mapped_column(
        ForeignKey("oap_propeditclasses_list.id")
    )
    # refs
    ref_title: Mapped[list["OapTextDB"]] = relationship()
    ref_propeditprops_list: Mapped[OapPropEditPropsListDB] = relationship()
    ref_propeditclasses_list: Mapped[OapPropEditClassesListDB] = relationship()
    ref_program: Mapped[OapProgramDB] = relationship()


class OapPropEditDB(SqlAlchemyBase):
    __tablename__ = "oap_propedit"
    __table_args__ = (UniqueConstraint("name", "program_id"),)
    # keys
    id: Mapped[int] = mapped_column(primary_key=True)
    program_id: Mapped[int] = mapped_column(
        ForeignKey("oap_program.id", ondelete="CASCADE")
    )
    title_id: Mapped[int | None] = mapped_column(ForeignKey("oap_text.id"))
    # scalars
    name: Mapped[str] = mapped_column(String(IDX_STRING_LENGTH)) 
    state_restr: Mapped[StateRestrType] = mapped_column(
        Enum(
            StateRestrType,
            values_callable=lambda obj: [
                e.value for e in obj
            ],  # Use the enum values in the DB
        )
    )
    properties: Mapped[str | None] = mapped_column(Text)
    classes: Mapped[str | None] = mapped_column(Text)
    # refs
    ref_title: Mapped[list["OapTextDB"]] = relationship()
    ref_program: Mapped[OapProgramDB] = relationship()


class OapPropChangeDB(SqlAlchemyBase):
    __tablename__ = "oap_propchange"
    __table_args__ = (UniqueConstraint("name", "program_id"),)
    # keys
    id: Mapped[int] = mapped_column(primary_key=True)
    program_id: Mapped[int] = mapped_column(
        ForeignKey("oap_program.id", ondelete="CASCADE")
    )
    # scalars
    name: Mapped[str] = mapped_column(String(IDX_STRING_LENGTH))
    type: Mapped[PropChangeType] = mapped_column(Enum(PropChangeType))
    property: Mapped[str] = mapped_column(String(STRING_LENGTH))
    value: Mapped[str] = mapped_column(String(STRING_LENGTH))
    # refs
    ref_program: Mapped[OapProgramDB] = relationship()


class OapMessageDB(SqlAlchemyBase):
    __tablename__ = "oap_message"
    __table_args__ = (UniqueConstraint("name", "program_id"),)
    # keys
    id: Mapped[int] = mapped_column(primary_key=True)
    program_id: Mapped[int] = mapped_column(
        ForeignKey("oap_program.id", ondelete="CASCADE")
    )
    text_id: Mapped[int | None] = mapped_column(ForeignKey("oap_text.id"))
    action_id: Mapped[int | None] = mapped_column(
        ForeignKey("oap_action.id", use_alter=True)
    )
    # sclars
    name: Mapped[str] = mapped_column(String(IDX_STRING_LENGTH))
    arg_type: Mapped[MessageArgType] = mapped_column(Enum(MessageArgType))
    # refs
    ref_text: Mapped["OapTextDB"] = relationship()
    ref_action: Mapped["OapActionDB"] = relationship(foreign_keys=[action_id])
    ref_program: Mapped[OapProgramDB] = relationship()


class OapMethodCallDB(SqlAlchemyBase):
    __tablename__ = "oap_methodcall"
    __table_args__ = (UniqueConstraint("name", "program_id"),)
    # keys
    id: Mapped[int] = mapped_column(primary_key=True)
    program_id: Mapped[int] = mapped_column(
        ForeignKey("oap_program.id", ondelete="CASCADE")
    )
    # scalars
    name: Mapped[str] = mapped_column(String(IDX_STRING_LENGTH))
    type: Mapped[MethodCallType] = mapped_column(Enum(MethodCallType))
    context: Mapped[str] = mapped_column(String(STRING_LENGTH))
    method: Mapped[str] = mapped_column(String(STRING_LENGTH))
    arguments: Mapped[str | None] = mapped_column(Text)
    ref_program: Mapped[OapProgramDB] = relationship()


class OapDimChangeDB(SqlAlchemyBase):
    __tablename__ = "oap_dimchange"
    __table_args__ = (UniqueConstraint("name", "program_id"),)
    # keys
    id: Mapped[int] = mapped_column(primary_key=True)
    program_id: Mapped[int] = mapped_column(
        ForeignKey("oap_program.id", ondelete="CASCADE")
    )
    # scalars
    name: Mapped[str] = mapped_column(String(IDX_STRING_LENGTH))
    dimension: Mapped[DimChangeDimension] = mapped_column(Enum(DimChangeDimension))
    condition: Mapped[str | None] = mapped_column(Text)
    separate: Mapped[str] = mapped_column(String(STRING_LENGTH))
    third_dim: Mapped[str] = mapped_column(String(STRING_LENGTH))
    property: Mapped[str] = mapped_column(String(STRING_LENGTH))
    multiplier: Mapped[str] = mapped_column(String(STRING_LENGTH))
    precision: Mapped[str] = mapped_column(String(STRING_LENGTH))
    ref_program: Mapped[OapProgramDB] = relationship()


class OapImageDB(SqlAlchemyBase):
    __tablename__ = "oap_image"
    __table_args__ = (UniqueConstraint("name", "program_id"),)
    # keys
    id: Mapped[int] = mapped_column(primary_key=True)
    program_id: Mapped[int] = mapped_column(
        ForeignKey("oap_program.id", ondelete="CASCADE")
    )
    # scalars
    name: Mapped[str] = mapped_column(String(IDX_STRING_LENGTH))
    image_de_dpr1: Mapped[str | None] = mapped_column(String(STRING_LENGTH))
    image_en_dpr1: Mapped[str | None] = mapped_column(String(STRING_LENGTH))
    image_fr_dpr1: Mapped[str | None] = mapped_column(String(STRING_LENGTH))
    image_nl_dpr1: Mapped[str | None] = mapped_column(String(STRING_LENGTH))
    image_xx_dpr1: Mapped[str | None] = mapped_column(String(STRING_LENGTH))
    image_de_dpr2: Mapped[str | None] = mapped_column(String(STRING_LENGTH))
    image_en_dpr2: Mapped[str | None] = mapped_column(String(STRING_LENGTH))
    image_fr_dpr2: Mapped[str | None] = mapped_column(String(STRING_LENGTH))
    image_nl_dpr2: Mapped[str | None] = mapped_column(String(STRING_LENGTH))
    image_xx_dpr2: Mapped[str | None] = mapped_column(String(STRING_LENGTH))
    ref_program: Mapped[OapProgramDB] = relationship()


class OapTextDB(SqlAlchemyBase):
    __tablename__ = "oap_text"
    __table_args__ = (UniqueConstraint("name", "program_id"),)
    # keys
    id: Mapped[int] = mapped_column(primary_key=True)
    program_id: Mapped[int] = mapped_column(
        ForeignKey("oap_program.id", ondelete="CASCADE")
    )
    # scalars
    name: Mapped[str] = mapped_column(String(IDX_STRING_LENGTH))
    text_de: Mapped[str | None] = mapped_column(Text)
    text_en: Mapped[str | None] = mapped_column(Text)
    text_fr: Mapped[str | None] = mapped_column(Text)
    text_nl: Mapped[str | None] = mapped_column(Text)
    ref_program: Mapped[OapProgramDB] = relationship()


class OapActionListActionAssocDB(SqlAlchemyBase):
    __tablename__ = "oap_actionlist_action"
    # keys
    actionlist_id: Mapped[int] = mapped_column(
        ForeignKey("oap_actionlist_item.id", ondelete="CASCADE"), primary_key=True
    )
    action_id: Mapped[int] = mapped_column(
        ForeignKey("oap_action.id"), primary_key=True
    )
    # program_id: Mapped[int] = mapped_column(ForeignKey("oap_program.id", ondelete="CASCADE"))
    # scalar
    position: Mapped[int]
    # refs
    ref_actionlist: Mapped["OapActionListItemDB"] = relationship(
        back_populates="ref_actions"
    )
    ref_action: Mapped["OapActionDB"] = relationship()
    # ref_program: Mapped[OapProgramDB] = relationship()


class OapInteractorActionAssocDB(SqlAlchemyBase):
    __tablename__ = "oap_interactor_action"
    # keys
    interactor_id: Mapped[int] = mapped_column(
        ForeignKey("oap_interactor.id"), primary_key=True
    )
    action_id: Mapped[int] = mapped_column(
        ForeignKey("oap_action.id"), primary_key=True
    )
    # program_id: Mapped[int] = mapped_column(ForeignKey("oap_program.id", ondelete="CASCADE"))
    # scalar
    position: Mapped[int]
    # refs
    ref_interactor: Mapped["OapInteractorDB"] = relationship()
    ref_action: Mapped["OapActionDB"] = relationship()
    # ref_program: Mapped[OapProgramDB] = relationship()


class OapActionListListDB(SqlAlchemyBase):
    __tablename__ = "oap_actionlist_list"
    __table_args__ = (UniqueConstraint("name", "program_id"),)
    # keys
    id: Mapped[int] = mapped_column(primary_key=True)
    program_id: Mapped[int] = mapped_column(
        ForeignKey("oap_program.id", ondelete="CASCADE")
    )
    # actionchoice_id: Mapped[int] = mapped_column(ForeignKey("oap_actionchoice.id")) # moved to actionchoice !
    # scalars
    name: Mapped[str] = mapped_column(String(IDX_STRING_LENGTH))
    # refs
    ref_actionlist: Mapped[list["OapActionListItemDB"]] = relationship(
        order_by="OapActionListItemDB.position"
    )
    ref_program: Mapped[OapProgramDB] = relationship()


class OapActionListItemDB(SqlAlchemyBase):
    __tablename__ = "oap_actionlist_item"
    __table_args__ = (UniqueConstraint("actionlistlist_id", "position", "program_id"),)
    # keys
    id: Mapped[int] = mapped_column(primary_key=True)
    program_id: Mapped[int] = mapped_column(
        ForeignKey("oap_program.id", ondelete="CASCADE")
    )
    text_id: Mapped[int | None] = mapped_column(ForeignKey("oap_text.id"))
    image_id: Mapped[int | None] = mapped_column(ForeignKey("oap_image.id"))
    actionlistlist_id: Mapped[int] = mapped_column(ForeignKey("oap_actionlist_list.id"))
    # scalar
    position: Mapped[int]
    condition: Mapped[str | None] = mapped_column(Text)
    # actions... n:m
    # refs
    ref_text: Mapped[OapTextDB] = relationship()
    ref_image: Mapped[OapImageDB] = relationship()
    ref_actions: Mapped[list[OapActionListActionAssocDB]] = relationship(
        back_populates="ref_actionlist",
        cascade="all, delete-orphan",  # Automatically delete associated rows
        passive_deletes=True,  # Optional: allows DB to handle deletions
    )
    # New direct relationship to OapActionDB without intermediary entity
    actions: Mapped[list["OapActionDB"]] = relationship(
        "OapActionDB",
        secondary="oap_actionlist_action",  # Name of the association table
        primaryjoin="OapActionListItemDB.id == OapActionListActionAssocDB.actionlist_id",
        secondaryjoin="OapActionDB.id == OapActionListActionAssocDB.action_id",
        order_by="OapActionListActionAssocDB.position.asc()", 
        viewonly=True,
    )
    ref_program: Mapped[OapProgramDB] = relationship()


class OapActionChoiceDB(SqlAlchemyBase):
    __tablename__ = "oap_actionchoice"
    __table_args__ = (UniqueConstraint("name", "program_id"),)
    # keys
    id: Mapped[int] = mapped_column(primary_key=True)
    program_id: Mapped[int] = mapped_column(
        ForeignKey("oap_program.id", ondelete="CASCADE")
    )
    title_id: Mapped[int | None] = mapped_column(ForeignKey("oap_text.id"))
    actionlist_id: Mapped[int | None] = mapped_column(
        ForeignKey("oap_actionlist_list.id")
    )
    # scalars
    name: Mapped[str] = mapped_column(String(IDX_STRING_LENGTH))
    view_type: Mapped[ActionChoiceViewType] = mapped_column(Enum(ActionChoiceViewType))
    argument: Mapped[ActionChoiceTileSize | None] = mapped_column(
        Enum(ActionChoiceTileSize)
    )
    # refs
    ref_actionlistlist: Mapped[OapActionListListDB] = relationship()
    ref_title: Mapped[OapTextDB | None] = relationship()
    ref_program: Mapped[OapProgramDB] = relationship()


class OapActionDB(SqlAlchemyBase):
    __tablename__ = "oap_action"
    __table_args__ = (UniqueConstraint("name", "program_id"),)
    # keys
    id: Mapped[int] = mapped_column(primary_key=True)
    program_id: Mapped[int] = mapped_column(
        ForeignKey("oap_program.id", ondelete="CASCADE")
    )
    # scalars
    name: Mapped[str] = mapped_column(String(IDX_STRING_LENGTH))
    condition: Mapped[str | None] = mapped_column(Text)
    type: Mapped[ActionType] = mapped_column(Enum(ActionType))
    # parameter....
    message_id: Mapped[int | None] = mapped_column(ForeignKey("oap_message.id"))
    dimchange_id: Mapped[int | None] = mapped_column(ForeignKey("oap_dimchange.id"))
    propchange_id: Mapped[int | None] = mapped_column(ForeignKey("oap_propchange.id"))
    propedit2_id: Mapped[int | None] = mapped_column(ForeignKey("oap_propedit2.id"))
    propedit_id: Mapped[int | None] = mapped_column(ForeignKey("oap_propedit.id"))
    extmedia_id: Mapped[int | None] = mapped_column(ForeignKey("oap_extmedia.id"))
    createobj_id: Mapped[int | None] = mapped_column(ForeignKey("oap_createobj.id"))
    methodcall_id: Mapped[int | None] = mapped_column(ForeignKey("oap_methodcall.id"))
    actionchoice_id: Mapped[int | None] = mapped_column(
        ForeignKey("oap_actionchoice.id")
    )
    ref_objects: Mapped[list[OapObjectDB]] = relationship(
        secondary=oap_action_object_association_table,
        cascade="all, delete"
    )
    #
    ref_message: Mapped[OapMessageDB | None] = relationship(foreign_keys=[message_id])
    ref_dimchange: Mapped[OapDimChangeDB | None] = relationship()
    ref_propchange: Mapped[OapPropChangeDB | None] = relationship()
    ref_propedit2: Mapped[OapPropEdit2DB | None] = relationship()
    ref_propedit: Mapped[OapPropEditDB | None] = relationship()
    ref_extmedia: Mapped[OapExtMediaDB | None] = relationship()
    ref_createobj: Mapped[OapCreateObjDB | None] = relationship()
    ref_methodcall: Mapped[OapMethodCallDB | None] = relationship()
    ref_actionchoice: Mapped[OapActionChoiceDB | None] = relationship()
    ref_program: Mapped[OapProgramDB] = relationship()


class OapArticle2TypeDB(SqlAlchemyBase):
    __tablename__ = "oap_article2type"
    __table_args__ = (UniqueConstraint("article_id", "program_id"),)
    # keys
    id: Mapped[int] = mapped_column(primary_key=True)
    program_id: Mapped[int] = mapped_column(
        ForeignKey("oap_program.id", ondelete="CASCADE")
    )
    # scalars
    manufacturer_id: Mapped[str] = mapped_column(String(STRING_LENGTH))
    series_id: Mapped[str] = mapped_column(String(STRING_LENGTH))
    article_id: Mapped[str]   = mapped_column(String(IDX_STRING_LENGTH))
    var_type: Mapped[str | None] = mapped_column(Text)
    variant: Mapped[str | None] = mapped_column(Text)
    type_id: Mapped[int] = mapped_column(ForeignKey("oap_type.id"))
    # refs
    ref_program: Mapped[OapProgramDB] = relationship()
    ref_type: Mapped["OapTypeDB"] = relationship()


class OapMetaType2TypeDB(SqlAlchemyBase):
    __tablename__ = "oap_metatype2type"
    __table_args__ = (UniqueConstraint("metatype_id", "program_id"),)
    # keys
    id: Mapped[int] = mapped_column(primary_key=True)
    program_id: Mapped[int] = mapped_column(
        ForeignKey("oap_program.id", ondelete="CASCADE")
    )
    # scalars
    manufacturer: Mapped[str] = mapped_column(String(STRING_LENGTH))
    series: Mapped[str] = mapped_column(String(STRING_LENGTH))
    metatype_id: Mapped[str]  = mapped_column(String(IDX_STRING_LENGTH))
    var_type: Mapped[str | None] = mapped_column(Text)
    variant: Mapped[str | None] = mapped_column(Text)
    type_id: Mapped[int] = mapped_column(ForeignKey("oap_type.id"))
    # refs
    ref_program: Mapped[OapProgramDB] = relationship()
    ref_type: Mapped["OapTypeDB"] = relationship()


class OapNumTripelDB(SqlAlchemyBase):
    __tablename__ = "oap_numtripel"
    __table_args__ = (UniqueConstraint("name", "program_id"),)
    # keys
    id: Mapped[int] = mapped_column(primary_key=True)
    program_id: Mapped[int] = mapped_column(
        ForeignKey("oap_program.id", ondelete="CASCADE")
    )
    # scalars
    name: Mapped[str] = mapped_column(String(IDX_STRING_LENGTH))
    x: Mapped[str] = mapped_column(Text)
    y: Mapped[str] = mapped_column(Text)
    z: Mapped[str] = mapped_column(Text)
    ref_program: Mapped[OapProgramDB] = relationship()


class OapSymbolDisplayDB(SqlAlchemyBase):
    __tablename__ = "oap_symboldisplay"
    # keys
    id: Mapped[int] = mapped_column(primary_key=True)
    program_id: Mapped[int] = mapped_column(
        ForeignKey("oap_program.id", ondelete="CASCADE")
    )
    interactor_id: Mapped[int] = mapped_column(ForeignKey("oap_interactor.id"))
    # scalars
    hidden_mode: Mapped[bool] = mapped_column(SmallInteger, default=False)
    offset_type: Mapped[OffsetType] = mapped_column(Enum(OffsetType))
    offset_id: Mapped[int | None] = mapped_column(ForeignKey("oap_numtripel.id"))
    offset_expr: Mapped[str | None] = mapped_column(Text)
    direction_id: Mapped[int | None] = mapped_column(ForeignKey("oap_numtripel.id"))
    view_angle: Mapped[str | None] = mapped_column(Text)
    orientation_x_id: Mapped[int | None] = mapped_column(ForeignKey("oap_numtripel.id"))
    # refs
    ref_offset: Mapped[OapNumTripelDB | None] = relationship(foreign_keys=[offset_id])
    ref_direction: Mapped[OapNumTripelDB | None] = relationship(
        foreign_keys=[direction_id]
    )
    ref_orientation_x: Mapped[OapNumTripelDB | None] = relationship(
        foreign_keys=[orientation_x_id]
    )
    ref_program: Mapped[OapProgramDB] = relationship()


oap_type_interactor_association_table = Table(
    "oap_type_interactor_association_table",
    SqlAlchemyBase.metadata,
    Column("oap_interactor_id", ForeignKey("oap_interactor.id"), primary_key=True),
    Column("oap_type_id", ForeignKey("oap_type.id"), primary_key=True),
)


class OapInteractorDB(SqlAlchemyBase):
    __tablename__ = "oap_interactor"
    __table_args__ = (UniqueConstraint("name", "program_id"),)
    # keys
    id: Mapped[int] = mapped_column(primary_key=True)
    program_id: Mapped[int] = mapped_column(
        ForeignKey("oap_program.id", ondelete="CASCADE")
    )
    # scalars
    name: Mapped[str] = mapped_column(String(IDX_STRING_LENGTH))
    condition: Mapped[str | None] = mapped_column(Text)
    needs_plan_mode: Mapped[str | None] = mapped_column(Text)
    # actions n:m
    symbol_type: Mapped[SymbolType] = mapped_column(Enum(SymbolType))
    symbol_size: Mapped[SymbolSize] = mapped_column(Enum(SymbolSize))
    # refs
    ref_symboldisplays: Mapped[list[OapSymbolDisplayDB]] = relationship()
    ref_actions: Mapped[list[OapInteractorActionAssocDB]] = relationship(
        back_populates="ref_interactor"
    )
    # New direct relationship to OapActionDB without intermediary entity
    actions: Mapped[list["OapActionDB"]] = relationship(
        "OapActionDB",
        secondary="oap_interactor_action",  # Name of the association table
        primaryjoin="OapInteractorDB.id == OapInteractorActionAssocDB.interactor_id",
        secondaryjoin="OapActionDB.id == OapInteractorActionAssocDB.action_id",
        order_by="OapInteractorActionAssocDB.position.asc()",
        viewonly=True,
    )
    ref_program: Mapped[OapProgramDB] = relationship()


class OapTypeDB(SqlAlchemyBase):
    __tablename__ = "oap_type"
    __table_args__ = (UniqueConstraint("name", "program_id"),)
    # keys
    id: Mapped[int] = mapped_column(primary_key=True)
    program_id: Mapped[int] = mapped_column(
        ForeignKey("oap_program.id", ondelete="CASCADE")
    )
    name: Mapped[str] = mapped_column(String(IDX_STRING_LENGTH))
    general_info: Mapped[str | None] = mapped_column(Text)
    prop_change_actions: Mapped[str | None] = mapped_column(Text)
    active_att_areas: Mapped[str | None] = mapped_column(Text)
    passive_att_areas: Mapped[str | None] = mapped_column(Text)
    # refs
    ref_interactor: Mapped[list[OapInteractorDB]] = relationship(
        "OapInteractorDB", secondary="oap_type_interactor_association_table"
    )
    ref_article2type: Mapped[list[OapArticle2TypeDB]] = relationship(
        "OapArticle2TypeDB",
        viewonly=True,
    )
    ref_metatype2type: Mapped[list[OapMetaType2TypeDB]] = relationship(
        "OapMetaType2TypeDB",
        viewonly=True,
    )
    ref_program: Mapped[OapProgramDB] = relationship()

    def deepcopy(self):
        copy = OapTypeDB()


# def shallow_copy(obj: SqlAlchemyBase):
#     print("shallow_copy", obj)
#     # class_ = obj.__class__
#     # new = class_()
#     # print("new...", new)
#     # kwargs = {
#     #     k: copy_orm_object(v)
#     #     for k, v in obj.__dict__.items()
#     #     if not k.startswith("_") and (no_ids == False or not k.endswith("id"))
#     # }


# shallow_copy(OapTypeDB(name="xxxx"))
 