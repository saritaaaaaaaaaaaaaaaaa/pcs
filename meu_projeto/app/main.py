from fastapi import FastAPI
from app.database import engine  # Volte a usar o "app."
from app import models           # Volte a usar o "app."

# Cria as tabelas automaticamente
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "O banco de dados foi inicializado com sucesso!"}
