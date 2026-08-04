from fastapi import APIRouter
from app.schemas.user import UserCreate
from app.services.user_service import register_user


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/")
def create_account(user: UserCreate):

    user_id = register_user(user)

    return {
        "id": user_id,
        "message": "Usuário criado"
    }