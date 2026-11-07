# Vamos fazer aqui com que o servidor do fastAPI crie as tabelas do banco de dados (ou estabeleça a conexão se já existir) toda vez que ele ligar, usaremos o recurso chamado lifespan para isso

from contextlib import asynccontextmanager
from fastapi import FastAPI
from backend.db import models #noqa: F401
from backend.db.database import create_db_and_tables # função que cria todas as tabelas que estão em models, pois lê os metadados para ver as tabelas registradas

@asynccontextmanager # define que é o inicio e o fim
async def lifespan(app:FastAPI):
    create_db_and_tables()
    yield # cria o banco de dados e deixa o servidor num estado de serving, até finalizar, quando finalizar, não executamos nada.

app = FastAPI(title="ComunicAI", lifespan=lifespan) # entrega a função lifespan para a aplicação usar

@app.get("/health")
def health():
    return {'status':"ok"}