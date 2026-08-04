import sqlite3
from pathlib import Path

from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app.models.user import User
from app.services.user_service import authenticate_user, register_user


router = APIRouter()
templates = Jinja2Templates(directory=Path(__file__).resolve().parent.parent / "templates")


@router.get("/cadastro")
def cadastro_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="cadastro.html",
        context={"error": request.query_params.get("error")},
    )


@router.post("/register")
def register(
    nome: str = Form(...),
    email: str = Form(...),
    senha: str = Form(...),
    data_nascimento: str = Form(...),
    telefone: str | None = Form(None),
    nivel: str = Form(...),
):
    user = User(None, nome, email, data_nascimento, telefone, nivel, True, senha)
    try:
        register_user(user)
    except sqlite3.IntegrityError:
        return RedirectResponse("/cadastro?error=email", status_code=303)
    return RedirectResponse("/login?error=registered", status_code=303)


@router.post("/login")
def login(request: Request, email: str = Form(...), senha: str = Form(...)):
    user = authenticate_user(email, senha)
    if user is None:
        return RedirectResponse("/login?error=invalid", status_code=303)
    request.session["user"] = {"id": user["id"], "nome": user["nome"], "email": user["email"]}
    return RedirectResponse("/", status_code=303)


@router.post("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/", status_code=303)
