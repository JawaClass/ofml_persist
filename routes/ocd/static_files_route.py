from fastapi import APIRouter
from fastapi.staticfiles import StaticFiles


router = APIRouter(prefix="/static")

router.mount(
    "/ocd_images",
    StaticFiles(
        directory="/mnt/knps_testumgebung/ofml_development/repository/kn/basics/DE/2/mat"
    ),
    name="ocd_images",
)
