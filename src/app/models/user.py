from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class User:
    id: Optional[int]
    nome: str
    email: str
    data_nascimento: date
    telefone: Optional[str]
    nivel: str
    ativo: bool
    senha_hash: str