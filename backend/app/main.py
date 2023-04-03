import uvicorn
from fastapi import APIRouter, FastAPI
from app.config import db
from app.service.auth_service import generate_role


def init_app():
    db.init()

    app = FastAPI(
        title="Fastapi login app",
        description="Login page",
        version="1"
    )

    @app.on_event("startup")
    async def startup():
        await db.create_all()
        await generate_role()

    @app.on_event("shutdown")
    async def shutdown():
        await db.close()

    return app


app = init_app()


def start():
    """Launched with 'poetry run start' at root level """
    uvicorn.run("app.main:app", host="localhost", port=8888, reload=True)
