from fastapi import UploadFile
from pydantic import BaseModel, ConfigDict, Field
from fastapi_filter.contrib.sqlalchemy import Filter
from api_models.oap import OapBaseFilter
from models.oap import OapImageDB


class OapImageFilter(OapBaseFilter):
    pass

    class Constants(Filter.Constants):
        model = OapImageDB


class OapImageCreate(BaseModel):
    program_id: int
    name: str
    image_de_dpr1: str | None = None
    image_en_dpr1: str | None = None
    image_fr_dpr1: str | None = None
    image_nl_dpr1: str | None = None
    image_xx_dpr1: str | None = None
    image_de_dpr2: str | None = None
    image_en_dpr2: str | None = None
    image_fr_dpr2: str | None = None
    image_nl_dpr2: str | None = None
    image_xx_dpr2: str | None = None

    model_config = ConfigDict(from_attributes=True)


class OapImageUpdate(OapImageCreate):
    id: int


class OapImageOut(OapImageUpdate):
    pass


class OapImageFileUpload(BaseModel):
    image: OapImageUpdate
    dpr: int
    language: str
    model_config = ConfigDict(from_attributes=True)
