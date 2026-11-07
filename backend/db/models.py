# Aqui é onde vamos colocar os esquemas das tabelas, que irão no catálogo, o catálogo é lido no db.py e usado para criar as tabelas no início do servidor

from datetime import datetime, timezone # usado pra log
from sqlmodel import Field, SQLModel
from enum import Enum
from sqlalchemy import JSON, Column

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
    position: int 
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

class SessionStatus(str, Enum):
    IN_PROGRESS = "em_andamento"
    COMPLETED = "concluido"

class ExerciseSession(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    exercise_id: int = Field(foreign_key="exercise.id", index=True)
    status: SessionStatus = Field(default=SessionStatus.IN_PROGRESS)
    current_question: int = Field(default=1)
    current_attempt: int = Field(default=1)
    started_at: datetime = Field(default_factory = utc_now)
    finished_at: datetime | None = None

class MessageRole(str, Enum):
    PERSONA = "persona"
    USER = "usuario"

class Message(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    session_id: int = Field(foreign_key="exercisesession.id", index=True)
    role: MessageRole
    content: str
    created_at: datetime = Field(default_factory=utc_now)

# As tabelas anteriores guardavam as perguntas de cada exercício, dados do usuario etc. Agora as tabelas abaixo irão guardar as avaliações, o mais importante.

class Attempt(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    session_id: int = Field(foreign_key="exercisesession.id", index=True)
    question_id: int = Field(foreign_key="question.id")
    attempt_number : int 
    answer: str
    scores: dict = Field(sa_column=Column(JSON))
    overall_score: float
    strengths: str 
    improvements: str 
    created_at: datetime = Field(default_factory=utc_now)


class QuestionOutcome(str, Enum):
    PASSED_FIRST = "aprovado_na_primeira"
    IMPROVED = "melhorou"
    NOT_IMPROVED = "nao_melhorou"

class QuestionResult(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    session_id: int = Field(foreign_key = "exercisesession.id", index=True)
    question_id: int = Field(foreign_key="question.id")
    outcome: QuestionOutcome
    encouragement_id: int | None = Field(default=None, foreign_key="encouragement.id")
    created_at: datetime = Field(default_factory=utc_now)