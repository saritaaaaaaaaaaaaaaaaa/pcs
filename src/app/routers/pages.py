from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from app.repositories.recipe_repository import (
    get_categories,
    get_difficulties,
    get_latest_recipes,
    get_recipes_by_filters,
    get_top_rated_recipes,
)

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


@router.get("/receitas", name="receitas")
def recipes_page(
    request: Request,
    titulo: str = "",
    categoria_id: str | None = None,
    dificuldade: str = "",
):
    """Lista receitas reais do banco e aplica os filtros recebidos por query string."""
    selected_category_id = int(categoria_id) if categoria_id and categoria_id.isdigit() else None
    has_filters = bool(titulo.strip() or selected_category_id is not None or dificuldade.strip())

    return templates.TemplateResponse(
        request=request,
        name="receitas.html",
        context={
            "user": request.session.get("user"),
            "categories": get_categories(),
            "difficulties": get_difficulties(),
            "filters": {
                "titulo": titulo,
                "categoria_id": selected_category_id,
                "dificuldade": dificuldade,
            },
            "filtered_recipes": get_recipes_by_filters(titulo, selected_category_id, dificuldade)
            if has_filters
            else [],
            "has_filters": has_filters,
            "latest_recipes": get_latest_recipes(),
            "top_rated_recipes": get_top_rated_recipes(),
        },
    )
