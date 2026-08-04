from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from app.database import create_tables
from app.routers import auth, pages


APP_DIR = Path(__file__).resolve().parent


@asynccontextmanager
async def lifespan(_: FastAPI):
    create_tables()
    yield


app = FastAPI(lifespan=lifespan)
app.add_middleware(SessionMiddleware, secret_key="troque-esta-chave-por-uma-segura")
app.mount("/static", StaticFiles(directory=APP_DIR / "static"), name="static")
app.include_router(pages.router)
app.include_router(auth.router)
