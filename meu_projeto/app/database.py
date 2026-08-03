from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define o nome do arquivo do banco de dados SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# O argumento 'check_same_thread' é necessário apenas para o SQLite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()  