from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional


class UserCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    data_nascimento: date
    telefone: Optional[str] = None
    nivel: str


class UserLogin(BaseModel):
    email: EmailStr
    senha: str


class UserResponse(BaseModel):
    id: int
    nome: str
    email: EmailStr
    data_nascimento: date
    telefone: Optional[str]
    nivel: str
    ativo: bool