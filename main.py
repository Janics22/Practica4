from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from db.db import create_db_and_tables
from routers import user


@asynccontextmanager
async def lifespan(_: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(
    title="Sample user API",
    description="API for managing user data",
    version="0.1.0",
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
    lifespan=lifespan,
)

app.include_router(user.router)

@app.get("/")
async def root() -> RedirectResponse:
    return RedirectResponse(url="/docs")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)