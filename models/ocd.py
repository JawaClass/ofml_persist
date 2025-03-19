# from sqlalchemy import select
from typing import List
from sqlalchemy import (
    Enum,
    ForeignKey,
    SmallInteger,
    UniqueConstraint,
    DateTime,
    and_,
    func,
)
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from models.base import SqlAlchemyBase
import enum


class TextType(enum.Enum):
    SHORT = "short"
    LONG = "long"
    PROP = "prop"
    PROPVALUE = "propvalue"
    PRICE = "price"
    PROPCLASS = "propclass"
    PROPHINT = "prophint"
    USERMESSAGE = "usermessage"


class ProgramPermission(enum.Enum):
    VIEW = "view"
    WRITE = "write"


class UserRole(enum.Enum):
    USER = "user"
    READ_ONLY_USER = "user"
    ADMIN = "admin"


class OfmlRegistryDB(SqlAlchemyBase):
    __tablename__ = "ofml_registry"
    id: Mapped[int] = mapped_column(primary_key=True)
    manufacturer: Mapped[str | None]
    manufacturer_id: Mapped[str | None]
    manufacturer_name: Mapped[str | None]
    program: Mapped[str | None]
    program_name: Mapped[str | None]
    program_id: Mapped[str | None]
    type: Mapped[str | None]
    category: Mapped[str | None]
    languages: Mapped[str | None]
    distribution_region: Mapped[str | None]
    version: Mapped[str | None]
    release_version: Mapped[str | None]
    release_date: Mapped[str | None]
    release_timestamp: Mapped[str | None]
    cat_type: Mapped[str | None]
    pd_format: Mapped[str | None]
    proginfo: Mapped[str | None]
    proginfodb_path: Mapped[str | None]
    depend: Mapped[str | None]
    geo_export_params: Mapped[str | None]
    persistency_form: Mapped[str | None]
    insertion_mode: Mapped[str | None]
    sql_db_program: Mapped[str | None]
    productdb: Mapped[str | None]
    productdb_path: Mapped[str | None]
    oam_path: Mapped[str | None]
    series_type: Mapped[str | None]
    meta_type: Mapped[str | None]
    catalogs: Mapped[str | None]
    release_state: Mapped[str | None]
    gf_version: Mapped[str | None]
    features: Mapped[str | None]
    mddb_path: Mapped[str | None]
    layer_progid_2d: Mapped[str | None]
    layer_progid_3d: Mapped[str | None]
    block_progid_2d: Mapped[str | None]
    block_progid_3d: Mapped[str | None]
    oap_program: Mapped[str | None]


class OcdProgramUserAssocDB(SqlAlchemyBase):
    __tablename__ = "ocd_program_user"
    __table_args__ = (UniqueConstraint("program_id", "user_id"),)
    # keys
    id: Mapped[int] = mapped_column(primary_key=True)
    program_id: Mapped[int] = mapped_column(
        ForeignKey("ocd_program.id", ondelete="CASCADE")
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("ocd_user.id", ondelete="CASCADE"))
    permission: Mapped[str] = mapped_column(Enum(ProgramPermission), index=True)


class OcdUserDB(SqlAlchemyBase):
    __tablename__ = "ocd_user"
    __table_args__ = (UniqueConstraint("email"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str]
    hashed_password: Mapped[str | None]
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole), index=True, default=UserRole.USER
    )
    create_date: Mapped[str] = mapped_column(DateTime, server_default=func.now())
    disabled: Mapped[bool] = mapped_column(SmallInteger, default=False)
    ref_programs = relationship(
        "OcdProgramDB", secondary=OcdProgramUserAssocDB.__table__
    )


class OcdProgramDB(SqlAlchemyBase):
    __tablename__ = "ocd_program"
    __table_args__ = (UniqueConstraint("name"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    registry_id: Mapped[int | None] = mapped_column(ForeignKey("ofml_registry.id"))
    creator_id: Mapped[int | None] = mapped_column(ForeignKey("ocd_user.id"))
    name: Mapped[str]
    description: Mapped[str | None]
    import_path: Mapped[str | None]
    create_date: Mapped[str] = mapped_column(DateTime, server_default=func.now())
    # refs
    ref_creator = relationship("OcdUserDB")
    ref_registry: Mapped[OfmlRegistryDB | None] = relationship("OfmlRegistryDB")
    ref_articles = relationship(
        "OcdArticleDB",
        back_populates="ref_program",
        cascade="all, delete-orphan",
    )


class OcdClassificationDB(SqlAlchemyBase):
    __tablename__ = "ocd_classification"
    # keys
    id: Mapped[int] = mapped_column(primary_key=True)
    article_id: Mapped[int] = mapped_column(
        ForeignKey("ocd_article.id", ondelete="CASCADE"), index=True
    )
    class_id: Mapped[int] = mapped_column(
        ForeignKey("ocd_propertyclass.id"), index=True
    )
    # scalars
    system: Mapped[str]


class OcdGlobalPackagingDB(SqlAlchemyBase):
    __tablename__ = "ocd_global_packaging"
    # keys
    id: Mapped[int] = mapped_column(primary_key=True)
    program_id: Mapped[int] = mapped_column(
        ForeignKey("ocd_program.id", ondelete="CASCADE")
    )
    # scalars
    var_cond: Mapped[str | None]
    width: Mapped[str | None]
    height: Mapped[str | None]
    depth: Mapped[str | None]
    measure_unit: Mapped[str | None]
    volume: Mapped[str | None]
    volume_unit: Mapped[str | None]
    tara_weight: Mapped[str | None]
    net_weight: Mapped[str | None]
    weight_unit: Mapped[str]
    items_per_unit: Mapped[str | None]
    pack_units: Mapped[str | None]
    # refs
    ref_program = relationship(
        "OcdProgramDB",
    )


class OcdPackagingDB(SqlAlchemyBase):
    __tablename__ = "ocd_packaging"
    __table_args__ = (UniqueConstraint("article_id"),)
    # keys
    id: Mapped[int] = mapped_column(primary_key=True)
    article_id: Mapped[int] = mapped_column(
        ForeignKey("ocd_article.id", ondelete="CASCADE"), index=True
    )
    # scalars
    var_cond: Mapped[str | None]
    width: Mapped[str | None]
    height: Mapped[str | None]
    depth: Mapped[str | None]
    measure_unit: Mapped[str | None]
    volume: Mapped[str | None]
    volume_unit: Mapped[str | None]
    tara_weight: Mapped[str | None]
    net_weight: Mapped[str | None]
    weight_unit: Mapped[str]
    items_per_unit: Mapped[str | None]
    pack_units: Mapped[str]


class OcdCodeSchemeDB(SqlAlchemyBase):
    __tablename__ = "ocd_codescheme"
    # keys
    id: Mapped[int] = mapped_column(primary_key=True)
    # scalars
    scheme: Mapped[str]
    varcode_sep: Mapped[str]
    value_sep: Mapped[str]
    visibility: Mapped[str]
    invisible_char: Mapped[str]
    unselect_char: Mapped[str]
    trim: Mapped[int] = mapped_column(SmallInteger)
    mo_sep: Mapped[str]
    mo_bracket: Mapped[str]


class OcdTaxSchemeDB(SqlAlchemyBase):
    __tablename__ = "ocd_taxscheme"
    # keys
    id: Mapped[int] = mapped_column(primary_key=True)
    # scalars
    country: Mapped[str]
    region: Mapped[str | None]
    number: Mapped[int] = mapped_column(SmallInteger)
    tax_type: Mapped[str]
    tax_category: Mapped[str]


class OcdArticleTaxesDB(SqlAlchemyBase):
    __tablename__ = "ocd_articletaxes"
    __table_args__ = (UniqueConstraint("article_id", "tax_id"),)
    # keys
    id: Mapped[int] = mapped_column(primary_key=True)
    # scalars
    article_id: Mapped[str] = mapped_column(
        ForeignKey("ocd_article.id", ondelete="CASCADE"), index=True
    )
    tax_id: Mapped[str] = mapped_column(ForeignKey("ocd_taxscheme.id"), index=True)
    date_from: Mapped[str | None]
    date_to: Mapped[str | None]
    # refs
    ref_taxscheme: Mapped[OcdTaxSchemeDB] = relationship("OcdTaxSchemeDB")


class OcdVersionDB(SqlAlchemyBase):
    __tablename__ = "ocd_version"
    # keys
    id: Mapped[int] = mapped_column(primary_key=True)
    # scalars
    format_version: Mapped[str]
    rel_coding: Mapped[str]
    data_version: Mapped[str]
    date_from: Mapped[str]
    date_to: Mapped[str]
    region: Mapped[str]
    varcond_var: Mapped[str]
    placeholder_on: Mapped[int] = mapped_column(SmallInteger)
    tables: Mapped[str]
    comment: Mapped[str]


class OcdPropertyValueDB(SqlAlchemyBase):
    __tablename__ = "ocd_propertyvalue"
    # keys
    id: Mapped[int] = mapped_column(primary_key=True)
    # property_class_id: Mapped[int] = mapped_column(
    #     ForeignKey("ocd_propertyclass.id"), index=True
    # )
    property_id: Mapped[int] = mapped_column(
        ForeignKey("ocd_property.id", ondelete="CASCADE"), index=True
    )
    text_id: Mapped[int | None] = mapped_column(ForeignKey("ocd_text.id"), index=True)
    relobj_id: Mapped[int | None] = mapped_column(
        ForeignKey("ocd_relationobj.id"), index=True
    )
    # scalars
    pos_pval: Mapped[int] = mapped_column(SmallInteger)
    is_default: Mapped[int] = mapped_column(SmallInteger)
    suppress_txt: Mapped[int] = mapped_column(SmallInteger)
    op_from: Mapped[str]
    value_from: Mapped[str | None]
    op_to: Mapped[str | None]
    value_to: Mapped[str | None]
    raster: Mapped[str | None]
    disabled: Mapped[bool] = mapped_column(SmallInteger, default=False)
    # refs
    ref_text: Mapped["OcdTextDB"] = relationship("OcdTextDB")
    ref_property: Mapped["OcdPropertyDB"] = relationship(
        "OcdPropertyDB", back_populates="ref_property_value"
    )
    # ref_property_class: Mapped["OcdPropertyClassDB"] = relationship(
    #     "OcdPropertyClassDB"
    # )
    ref_relationobj: Mapped["OcdRelationObjDB"] = relationship("OcdRelationObjDB")


class OcdPropertyDB(SqlAlchemyBase):
    __tablename__ = "ocd_property"
    # keys
    id: Mapped[int] = mapped_column(primary_key=True)
    property_class_id: Mapped[int] = mapped_column(
        ForeignKey("ocd_propertyclass.id", ondelete="CASCADE"), index=True
    )
    text_id: Mapped[int | None] = mapped_column(ForeignKey("ocd_text.id"), index=True)
    text_hint_id: Mapped[int | None] = mapped_column(ForeignKey("ocd_text.id"))
    relobj_id: Mapped[int | None] = mapped_column(
        ForeignKey("ocd_relationobj.id"), index=True
    )
    # scalars
    property: Mapped[str] = mapped_column(index=True)
    pos_prop: Mapped[int] = mapped_column(SmallInteger)
    prop_type: Mapped[str]
    digits: Mapped[int] = mapped_column(SmallInteger)
    dec_digits: Mapped[int] = mapped_column(SmallInteger)
    need_input: Mapped[int] = mapped_column(SmallInteger)
    add_values: Mapped[int] = mapped_column(SmallInteger)
    restrictable: Mapped[int] = mapped_column(SmallInteger)
    multi_option: Mapped[int] = mapped_column(SmallInteger)
    scope: Mapped[str]
    txt_control: Mapped[str]
    # refs
    ref_text: Mapped["OcdTextDB"] = relationship("OcdTextDB", foreign_keys=[text_id])
    ref_text_hint: Mapped["OcdTextDB"] = relationship(
        "OcdTextDB", foreign_keys=[text_hint_id]
    )
    ref_relationobj: Mapped["OcdRelationObjDB"] = relationship("OcdRelationObjDB")
    ref_property_value: Mapped[list[OcdPropertyValueDB]] = relationship(
        "OcdPropertyValueDB",
        back_populates="ref_property",
        cascade="all, delete-orphan",
    )
    ref_property_class: Mapped["OcdPropertyClassDB"] = relationship(
        "OcdPropertyClassDB", back_populates="ref_properties"
    )


class OcdPropertyClassDB(SqlAlchemyBase):
    __tablename__ = "ocd_propertyclass"
    # keys
    id: Mapped[int] = mapped_column(primary_key=True)
    text_id: Mapped[int | None] = mapped_column(ForeignKey("ocd_text.id"))
    relobj_id: Mapped[int | None] = mapped_column(ForeignKey("ocd_relationobj.id"))
    # scalars
    pos_class: Mapped[int]
    prop_class: Mapped[str]
    # refs
    ref_text: Mapped["OcdTextDB"] = relationship("OcdTextDB")
    ref_properties: Mapped[list[OcdPropertyDB]] = relationship(
        "OcdPropertyDB",
        back_populates="ref_property_class",
        cascade="all, delete-orphan",
    )


class OcdArticlePropertyclassAssocDB(SqlAlchemyBase):
    __tablename__ = "ocd_article_propertyclass"
    __table_args__ = (UniqueConstraint("article_id", "propertyclass_id"),)
    # keys
    id: Mapped[int] = mapped_column(primary_key=True)
    article_id: Mapped[int] = mapped_column(
        ForeignKey("ocd_article.id", ondelete="CASCADE")
    )
    propertyclass_id: Mapped[int] = mapped_column(
        ForeignKey("ocd_propertyclass.id", ondelete="CASCADE")
    )


class OcdPriceDB(SqlAlchemyBase):
    __tablename__ = "ocd_price"
    # keys
    id: Mapped[int] = mapped_column(primary_key=True)
    article_id: Mapped[int] = mapped_column(
        ForeignKey("ocd_article.id", ondelete="CASCADE"), index=True
    )
    # scalars
    var_cond: Mapped[str | None]
    price_type: Mapped[str]
    price_level: Mapped[str]
    price_rule: Mapped[str | None]
    price_text_id: Mapped[int | None] = mapped_column(ForeignKey("ocd_text.id"))
    price: Mapped[str]
    is_fix: Mapped[int]
    currency: Mapped[str]
    date_from: Mapped[str]
    date_to: Mapped[str]
    scale_quantity: Mapped[int]
    rounding_id: Mapped[int | None] = mapped_column(ForeignKey("ocd_rounding.id"))
    # refs
    ref_text: Mapped["OcdTextDB"] = relationship(
        "OcdTextDB", foreign_keys=[price_text_id]
    )
    ref_rounding: Mapped["OcdRoundingDB"] = relationship("OcdRoundingDB")


class OcdRoundingDB(SqlAlchemyBase):
    __tablename__ = "ocd_rounding"
    # keys
    id: Mapped[int] = mapped_column(primary_key=True)
    # scalars
    nr: Mapped[int]
    min: Mapped[str]
    max: Mapped[str]
    type: Mapped[str]
    precision: Mapped[float]
    add_before: Mapped[float]
    add_after: Mapped[float]


class OcdTextDB(SqlAlchemyBase):
    __tablename__ = "ocd_text"
    # keys
    id: Mapped[int] = mapped_column(primary_key=True)
    program_id: Mapped[int] = mapped_column(
        ForeignKey("ocd_program.id", ondelete="CASCADE")
    )
    # scalars
    text_type: Mapped[str] = mapped_column(Enum(TextType), index=True)
    text_de: Mapped[str | None]
    text_en: Mapped[str | None]
    text_fr: Mapped[str | None]
    text_nl: Mapped[str | None]
    ref_program = relationship("OcdProgramDB")


class OcdRelationObjRelationAssocDB(SqlAlchemyBase):
    __tablename__ = "ocd_relationobj_relation"
    __table_args__ = (UniqueConstraint("relationobj_id", "relation_id", "rel_type"),)
    # keys
    id: Mapped[int] = mapped_column(primary_key=True)
    relationobj_id: Mapped[int] = mapped_column(
        ForeignKey("ocd_relationobj.id", ondelete="CASCADE")
    )
    relation_id: Mapped[int] = mapped_column(
        ForeignKey("ocd_relation.id", ondelete="CASCADE")
    )
    # scalars
    position: Mapped[int]
    rel_type: Mapped[int]
    rel_domain: Mapped[str]
    # refs
    ref_relation = relationship(
        "OcdRelationDB",  # back_populates="ref_relationobj_relation_assoc"
    )
    ref_relationobj = relationship(
        "OcdRelationObjDB", back_populates="ref_relationobj_relation_assoc"
    )


class OcdRelationDB(SqlAlchemyBase):
    __tablename__ = "ocd_relation"
    # keys
    id: Mapped[int] = mapped_column(primary_key=True)
    # scalars
    name: Mapped[str | None]
    rel_block: Mapped[str]


class OcdRelationObjDB(SqlAlchemyBase):
    __tablename__ = "ocd_relationobj"
    # keys
    id: Mapped[int] = mapped_column(primary_key=True)
    # scalars
    name: Mapped[str | None]
    # refs
    ref_relationobj_relation_assoc: Mapped[list[OcdRelationObjRelationAssocDB]] = (
        relationship("OcdRelationObjRelationAssocDB", back_populates="ref_relationobj")
    )


class OcdArtbaseDB(SqlAlchemyBase):
    __tablename__ = "ocd_artbase"
    __table_args__ = (
        UniqueConstraint("article_id", "class_name", "prop_name", "prop_value"),
    )
    # keys
    id: Mapped[int] = mapped_column(primary_key=True)
    article_id: Mapped[int] = mapped_column(
        ForeignKey("ocd_article.id", ondelete="CASCADE")
    )
    # scalars
    class_name: Mapped[str]
    prop_name: Mapped[str]
    prop_value: Mapped[str]


class OcdUtilArticleClonedSourceDB(SqlAlchemyBase):
    __tablename__ = "ocd_util_article_cloned_source"
    __table_args__ = (UniqueConstraint("article_id"),)
    # keys
    id: Mapped[int] = mapped_column(primary_key=True)
    article_id: Mapped[int | None] = mapped_column(
        ForeignKey("ocd_article.id", ondelete="CASCADE"), index=True
    )
    src_article_nr: Mapped[str] = mapped_column(index=True)
    src_series: Mapped[str] = mapped_column(index=True)


class OcdArticleDB(SqlAlchemyBase):
    __tablename__ = "ocd_article"
    __table_args__ = (UniqueConstraint("article_nr", "program_id"),)
    # keys
    id: Mapped[int] = mapped_column(primary_key=True)
    short_text_id: Mapped[int | None] = mapped_column(
        ForeignKey("ocd_text.id"), index=True
    )
    long_text_id: Mapped[int | None] = mapped_column(
        ForeignKey("ocd_text.id"), index=True
    )
    relobj_id: Mapped[int | None] = mapped_column(ForeignKey("ocd_relationobj.id"))
    program_id: Mapped[int] = mapped_column(
        ForeignKey("ocd_program.id", ondelete="CASCADE")
    )
    scheme_id: Mapped[str | None] = mapped_column(ForeignKey("ocd_codescheme.id"))
    # scalars
    article_nr: Mapped[str] = mapped_column(index=True)
    art_type: Mapped[str]
    manufacturer: Mapped[str]
    series: Mapped[str]
    fast_supply: Mapped[int] = mapped_column(default=0)
    discountable: Mapped[int] = mapped_column(default=1)
    order_unit: Mapped[str] = mapped_column(default="C62")
    # refs
    ref_short_text: Mapped[OcdTextDB | None] = relationship(
        "OcdTextDB",
        foreign_keys=[short_text_id],
    )
    ref_long_text: Mapped[OcdTextDB | None] = relationship(
        "OcdTextDB",
        foreign_keys=[long_text_id],
    )
    ref_relationobj: Mapped[OcdRelationObjDB | None] = relationship(
        "OcdRelationObjDB", foreign_keys=[relobj_id]
    )
    ref_artbase: Mapped[List[OcdArtbaseDB]] = relationship(
        "OcdArtbaseDB", cascade="all, delete"
    )
    ref_price: Mapped[List[OcdPriceDB]] = relationship(
        "OcdPriceDB", cascade="all, delete"
    )
    ref_propertyclasses: Mapped[List[OcdPropertyClassDB]] = relationship(
        "OcdPropertyClassDB",
        secondary=OcdArticlePropertyclassAssocDB.__table__,
        cascade="all, delete",
    )
    ref_articletaxes: Mapped[List[OcdArticleTaxesDB]] = relationship(
        "OcdArticleTaxesDB", cascade="all, delete"
    )
    ref_packaging: Mapped[OcdPackagingDB] = relationship(
        "OcdPackagingDB", cascade="all, delete"
    )
    ref_program: Mapped[OcdProgramDB] = relationship(
        "OcdProgramDB", back_populates="ref_articles"
    )
    ref_codescheme: Mapped[OcdCodeSchemeDB | None] = relationship("OcdCodeSchemeDB")
    ref_price_article_only_view: Mapped[List[OcdPriceDB]] = relationship(
        "OcdPriceDB",
        primaryjoin=and_(
            OcdPriceDB.article_id == id,  # Foreign key condition
            OcdPriceDB.price_level == "B",  # Filter condition
            OcdPriceDB.price_type == "S",  # Filter condition
            OcdPriceDB.var_cond == None,  # Filter condition
        ),
        viewonly=True,
    )

    ref_cloned_src: Mapped[OcdUtilArticleClonedSourceDB] = relationship(
        "OcdUtilArticleClonedSourceDB", cascade="all, delete"
    )
