from sqlmodel import Session, SQLModel, create_engine

from backend.core.config import settings 

connect_args = {}

if settings.database_url.startswith("sqlite"):
    connect_args = {"check_same_thread":False} # o fastapi usa varias threads, mas o sqlite so a que o abriu, aqui a gente desliga essa trava para eles poderem conversar bem entre si

engine = create_engine(settings.database_url, connect_args=connect_args) # aqui é o que a gente vai usar pra se conectar com o banco de fato, é a interface que vai permitir comunicar o banco de dados com o código 

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


# o engine é o que estabelece a comunicação com banco, já o Session são as conversas continuas com o banco, engine é só uma, ja cada pedido vira uma Session, seja ler dados, alterar dados etc.
# Cada requisição http deve ter sua propria sessão, para evitar conflito de dados.
# O fastapi usará essa função nas rotas, basicamente ela executa a função até o yieled, que consiste em abrir uma sessão com with, ela vai pausar ali e entregar para  a rota que pediu, que ira usar, apos isso terminar, o yield retorna e o with fecha a sessão

def get_session():
    with Session(engine) as session: 
        yield session