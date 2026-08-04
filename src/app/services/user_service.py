from app.repositories import user_repository
from app.utils.security import hash_password, verify_password


def register_user(user):

    user.senha_hash = hash_password(user.senha_hash)

    user_id = user_repository.create_user(user)

    return user_id


def authenticate_user(email: str, senha: str):
    user = user_repository.get_user_by_email(email)
    if user is None or not user["ativo"]:
        return None
    return user if verify_password(senha, user["senha_hash"]) else None
