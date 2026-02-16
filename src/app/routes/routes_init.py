from fastapi import FastAPI, APIRouter, status

import src.app.routes.v1 as v1_routes


def routes_init(app: FastAPI) -> None:
    app.include_router(v1_routes.auth_router)
    app.include_router(v1_routes.blogs_router)
    app.include_router(v1_routes.users_router)

    @app.get("/", status_code=status.HTTP_200_OK)
    def default_route():
        return {"message": "OK"}
