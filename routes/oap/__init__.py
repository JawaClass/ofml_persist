from fastapi.staticfiles import StaticFiles
import constants
from routes.oap import (
    interactor_route,
    program_route,
    type_route,
    action_route,
    methodcall_route,
    createobj_route,
    dimchange_route,
    message_route,
    propedit_route,
    article2type_route,
    metatype2type_route,
    actionchoice_route,
    actionlistheader_route,
    text_route,
    numtripel_route,
    extmedia_route,
    symboldisplay_route,
    propedit2_route,
    object_route,
    propedit2propslist_route,
    propedit2propslistitem_route,
    propedit2classeslist_route,
    propedit2classeslistitem_route,
    propchange_route,
    actionlistitem_route,
    image_route,
)


def include(app):

    # oap
    oap_prefix = "/oap"
    app.include_router(interactor_route.router, prefix=oap_prefix, tags=["oap"])
    app.include_router(type_route.router, prefix=oap_prefix, tags=["oap"])
    app.include_router(action_route.router, prefix=oap_prefix, tags=["oap"])
    app.include_router(methodcall_route.router, prefix=oap_prefix, tags=["oap"])
    app.include_router(createobj_route.router, prefix=oap_prefix, tags=["oap"])
    app.include_router(dimchange_route.router, prefix=oap_prefix, tags=["oap"])
    app.include_router(message_route.router, prefix=oap_prefix, tags=["oap"])
    app.include_router(propedit_route.router, prefix=oap_prefix, tags=["oap"])
    app.include_router(article2type_route.router, prefix=oap_prefix, tags=["oap"])
    app.include_router(metatype2type_route.router, prefix=oap_prefix, tags=["oap"])
    app.include_router(actionchoice_route.router, prefix=oap_prefix, tags=["oap"])
    app.include_router(actionlistheader_route.router, prefix=oap_prefix, tags=["oap"])
    app.include_router(text_route.router, prefix=oap_prefix, tags=["oap"])
    app.include_router(numtripel_route.router, prefix=oap_prefix, tags=["oap"])
    app.include_router(symboldisplay_route.router, prefix=oap_prefix, tags=["oap"])
    app.include_router(extmedia_route.router, prefix=oap_prefix, tags=["oap"])
    app.include_router(propedit2_route.router, prefix=oap_prefix, tags=["oap"])
    app.include_router(object_route.router, prefix=oap_prefix, tags=["oap"])
    app.include_router(propedit2propslist_route.router, prefix=oap_prefix, tags=["oap"])
    app.include_router(
        propedit2propslistitem_route.router, prefix=oap_prefix, tags=["oap"]
    )
    app.include_router(
        propedit2classeslist_route.router, prefix=oap_prefix, tags=["oap"]
    )
    app.include_router(
        propedit2classeslistitem_route.router, prefix=oap_prefix, tags=["oap"]
    )
    app.include_router(propchange_route.router, prefix=oap_prefix, tags=["oap"])
    app.include_router(actionlistitem_route.router, prefix=oap_prefix, tags=["oap"])
    app.include_router(program_route.router, prefix=oap_prefix, tags=["oap"])
    app.include_router(image_route.router, prefix=oap_prefix, tags=["oap"])

    app.mount(
        "/oap/image/files",
        StaticFiles(directory=constants.root_path / "resources/oap/images"),
        name="files",
    )

