from typing import Annotated, BinaryIO
from fastapi import APIRouter, Depends, File, Form, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi_filter import FilterDepends
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import delete, select
from sqlalchemy.orm import Session
from api_models.oap import OapBaseFilter
from api_models.oap.image import (
    OapImageCreate,
    OapImageFileUpload,
    OapImageFilter,
    OapImageOut,
    OapImageUpdate,
)
from api_models.util.model_scheme import get_simple_model_scheme
from models import generate_session
from models.oap import OapImageDB, OapMethodCallDB
from sqlalchemy.orm import joinedload
from fastapi_pagination import Page
from routes import util
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy import select, func
import constants

from routes.pagination import LargePage


router = APIRouter(prefix="/image")

@router.get("/scheme")
def read_scheme(extensive: bool = False):
    """
    return image scheme
    """
    scheme =  OapImageOut.model_json_schema() if extensive else get_simple_model_scheme(OapImageOut)
    return scheme

@router.get("/{image_id}", response_model=OapImageOut)
def read_image(
    image_id: int,
    session: Session = Depends(generate_session),
):
    """
    return image by id
    """
    select_stmt = select(OapImageDB).filter(OapImageDB.id == image_id)
    item = session.execute(select_stmt).scalar_one()
    return item


@router.get("")
def read_images(
    session: Session = Depends(generate_session),
    image_filter=FilterDepends(OapImageFilter),
) -> LargePage[OapImageOut]:
    """
    return all images
    """
    return paginate(session, image_filter.filter(select(OapImageDB)))


@router.put("")
def update_image(
    image: OapImageUpdate,
    session: Session = Depends(generate_session),
):
    """
    update image
    """
    return util.exec_simple_update(OapImageDB, session, image)


@router.delete("/{image_id}")
def delete_image(
    image_id: int,
    session: Session = Depends(generate_session),
):
    """
    delete image
    """
    return util.exec_simple_delete(OapImageDB, session, image_id)


@router.post("")
def create_image(image: OapImageCreate, session: Session = Depends(generate_session)):
    """
    create image
    """
    image = util.exec_simple_insert(OapImageDB, session, image)
    image.image_xx_dpr1
    dpr = 1
    language = "xx"
    filename = "no_image.png"

    with open(constants.root_path / "resources/oap/default_values" / filename, "b+r") as file:
        image = save_image_file(file, filename, image, language, dpr, session)

    return image




@router.post("/uploadfile")
def upload_image_file(
    file: UploadFile,
    image_id: int = Form(),
    language: str = Form(),
    dpr: int = Form(),
    session: Session = Depends(generate_session),
):
    select_stmt = select(OapImageDB).filter(OapImageDB.id == image_id)
    image = session.execute(select_stmt).scalar_one()

    image = save_image_file(file.file, file.filename, image, language, dpr, session)

    return image


def save_image_file(
    file: BinaryIO,
    filename: str,
    image: OapImageDB,
    language: str,
    dpr: int,
    session: Session) -> OapImageDB:

    img_folder = rf"images/{language}/tile_medium_dpr{dpr}"

    setattr(image, f"image_{language}_dpr{dpr}", f"{img_folder}/{filename}")
    session.add(image)
    session.commit()

    dst_images_folder = (
        constants.root_path
        / "resources/oap/images"
        / image.ref_program.name
        / img_folder
    )

    dst_path_image = dst_images_folder / filename

    print("dst_images_folder:", dst_images_folder, "::", dst_images_folder.exists())

    if not dst_images_folder.exists():
        dst_images_folder.mkdir(parents=True)

    print("save file...", filename)
  
    file_bytes = file.read()
    with open(dst_path_image, "b+w") as f:
        f.write(file_bytes)

    return image