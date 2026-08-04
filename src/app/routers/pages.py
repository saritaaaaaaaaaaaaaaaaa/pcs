from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


router = APIRouter()
templates = Jinja2Templates(directory=Path(__file__).resolve().parent.parent / "templates")


@router.get("/", name="index")
def index_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"user": request.session.get("user")},
    )


@router.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={"error": request.query_params.get("error")},
    )
