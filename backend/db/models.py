# Aqui é onde vamos colocar os esquemas das tabelas, que irão no catálogo, o catálogo é lido no db.py e usado para criar as tabelas no início do servidor

from datetime import datetime, timezone # usado pra log
from sqlmodel import Field, SQLModel
from enum import Enum

def utc_now():
    return datetime.now(timezone.utc)

# Aqui a gente ta criando o esquema da tabela de fato, Field define quem vai ser atributo
class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=100)
    email: str = Field(unique=True, index=True, max_length=255)
    password_hash: str
    created_at: datetime = Field(default_factory=utc_now)

class ExerciseMode(str, Enum): # enum limita a quantidade de opções, pois alguem necessariamente precisa escolher entre escrita e fala, não há outra opção
    WRITING = "escrita"
    SPEAKING = "fala"

class Exercise(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(max_length=150)
    mode: ExerciseMode = Field(index=True)
    position = int 
    scenario: str
    persona: str
    objetctive: str
    active: bool = Field(default=True)

class Question(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    exercise_id: int = Field(foreign_key="exercise.id", index=True)
    position: int 
    text: str

class Encouragement(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    text: str = Field(max_length=300)
    active: bool = Field(default=True)



