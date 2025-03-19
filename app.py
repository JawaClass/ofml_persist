from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.exception_handlers import http_exception_handler
from fastapi.routing import APIRoute
from fastapi.staticfiles import StaticFiles
from routes.ocd import include as include_ocd_route
from routes.oap import include as include_oap_route
from routes.plaintext import profiles_route
from fastapi_pagination import add_pagination
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from services import auth_service
from constants import path_testumgebung
import traceback
app = FastAPI()
   
# @app.exception_handler(HTTPException)
# async def unicorn_exception_handler(request: Request, exc: HTTPException):
#     print("#" * 5, "ERROR")
#     print(f"  {exc}")
#     traceback.print_exception(type(exc), exc, exc.__traceback__)
#     # return JSONResponse(
#     #     status_code=exc.status_code,
#     #     content={"message": f"Oops! {exc.detail} did something. There goes a rainbow..."},
#     # )

#     # Use the default exception handler to return the standard response
#     return await http_exception_handler(request, exc)


# app.add_exception_handler(Exception, unicorn_exception_handler)

add_pagination(app)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
 
include_ocd_route(app)
include_oap_route(app)

app.mount("/static", StaticFiles(directory=path_testumgebung), name="static")

# plaintext
plaintext_prefix = "/plaintext"
app.include_router(profiles_route.router, prefix=plaintext_prefix, tags=["plaintext"])


@app.get("/")
def root():
    return {"message": "Hello World"}
 

# fastapi dev app.py
# uvicorn --host 0.0.0.0 --port 8000 --reload --workers 4 app:app

# DEBUG
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
