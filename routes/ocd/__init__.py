from routes.ocd import (
    article_route,
    artbase_route,
    text_route,
    price_route,
    property_route,
    propertyvalue_route,
    propertyclass_route,
    program_route,
    user_route,
    login_route,
    static_files_route,
)


def include(app):

    # ocd
    ocd_prefix = "/ocd"
    app.include_router(article_route.router, prefix=ocd_prefix, tags=["ocd"])
    app.include_router(artbase_route.router, prefix=ocd_prefix, tags=["ocd"])
    app.include_router(text_route.router, prefix=ocd_prefix, tags=["ocd"])
    app.include_router(price_route.router, prefix=ocd_prefix, tags=["ocd"])
    app.include_router(property_route.router, prefix=ocd_prefix, tags=["ocd"])
    app.include_router(propertyvalue_route.router, prefix=ocd_prefix, tags=["ocd"])
    app.include_router(propertyclass_route.router, prefix=ocd_prefix, tags=["ocd"])
    app.include_router(
        program_route.router,
        prefix=ocd_prefix,
        tags=["ocd"],
        # dependencies=[Depends(auth_service.oauth2_scheme)],
    )
    app.include_router(user_route.router, prefix=ocd_prefix, tags=["ocd"])
    app.include_router(login_route.router)
    app.include_router(static_files_route.router)
