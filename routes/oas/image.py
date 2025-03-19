from fastapi import APIRouter


router = APIRouter(prefix="/images")

# @router.get("/<article>")
# def load_image(article: str):
#     res: Resource
#     for res in Resource.query.filter(Resource.name == article).all():
#         image_folder = (
#             Config.IMPORT_PLAINTEXT_PATH
#             / str(res.sql_db_program)
#             / "DE"
#             / "2"
#             / "image"
#         )
#         image_file = image_folder / str(res.resource_path)
#         if image_file.exists():
#             return send_from_directory(image_folder, res.resource_path)

#     abort(404)
