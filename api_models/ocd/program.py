from typing import Any
from pydantic import BaseModel, ConfigDict, Field
from fastapi_filter.contrib.sqlalchemy import Filter
from .user import OcdUserOut
from models.ocd import OcdProgramDB


class OcdProgramFilter(Filter):
    order_by: list[str] | None = None
    name: str | None = None
    name__in: list[str] | None = None

    class Constants(Filter.Constants):
        model = OcdProgramDB


class OcdProgramCreate(BaseModel):
    name: str
    description: str | None = None
    import_path: str | None = None


class ArticleProgram(BaseModel):
    article_nr: str
    program: str


class OcdProgramCreateFromArticles(OcdProgramCreate):
    article_program_list: list[ArticleProgram]


class OcdProgramUpdate(OcdProgramCreate):
    id: int
    create_date: Any


class OcdProgramOut(OcdProgramCreate):
    id: int
    create_date: Any
    model_config = ConfigDict(from_attributes=True)


class OcdProgramWithCreatorOut(OcdProgramOut):
    ref_creator: OcdUserOut | None = None
