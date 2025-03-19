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

  
class OasResourceDB(SqlAlchemyBase):
    __tablename__ = "oas_resource"
    # keys
    id: Mapped[int] = mapped_column(primary_key=True) 
    article_id: Mapped[int] = mapped_column(ForeignKey("oas_article.id"))

class OasVariantDB(SqlAlchemyBase):
    __tablename__ = "oas_variant"
    # keys
    id: Mapped[int] = mapped_column(primary_key=True) 
    variant_code: Mapped[str | None]
    
    
class OasStructureDB(SqlAlchemyBase):
    __tablename__ = "oas_structure"
    __table_args__ = (UniqueConstraint("article_id"),)
    # keys
    id: Mapped[int] = mapped_column(primary_key=True)
    article_id: Mapped[int] = mapped_column(ForeignKey("oad_article.id"))
    variant_id: Mapped[int] = mapped_column(ForeignKey("oad_variant.id"))


class OasArticleDB(SqlAlchemyBase):
    __tablename__ = "oas_article"
    __table_args__ = (UniqueConstraint("article_nr", "program_id"),)
    # keys
    id: Mapped[int] = mapped_column(primary_key=True)
    item_key: Mapped[str] = mapped_column(index=True)
     