import json 
from pathlib import Path 
from sqlmodel import Session, select
from backend.db.database import create_db_and_tables, engine
from backend.db.models import Encouragement, Exercise, ExerciseMode, Question

SEED_FILE = Path(__file__).parent / "content" / "seed.json"

# Serve para verificar quais as frases do JSON que já estão no banco e quais não estão, as que não estão vão ser adicionadas
def seed_encouragements(session: Session, texts: list[str]):
    for text in texts: # varre todas as frases do JSON
        existing = session.exec(
            select(Encouragement).where(Encouragement.text == text) # Para cada frase do JSON verifica se já está no banco
        ).first()
        if existing is None: # Se não estiver, adiciona
            session.add(Encouragement(text==text))

def seed_exercises(session: Session, exercises: list[dict]):
    for data in exercises: # para cada exercicio dentro do json de exercícios
        questions = data.pop("questions") # retiramos as questões do json
        data["mode"] = ExerciseMode(data["mode"]) # atribuimos o atributo mode ao json de cada exercicio, em vez de ser uma simples string, vira um dos objetos do enum

        exercise = session.exec( # Procura utilizando o modo e a posição para ver se ja existe
            select(Exercise).where(
                Exercise.mode == data["mode"],
                Exercise.position == data["position"]
            )
        ).first()

        if exercise is None: # Se o exercício não existir, ele é criado, ao desempacotar o dicionário e adicionado no banco
            exercise = Exercise(**data)
            session.add(exercise)
        else:
            for field, value in data.items(): # equivale a dizer que para cada campo, para cada valor, atualizamos com o valor do dicionário, pro banco sempre ficar atualizado com o arquivo
                setattr(exercise, field, value)

        session.flush() # vai para o banco, busca colocar um id, se não conseguir tudo é desfeito

        for position, text in enumerate(questions, start=1): # percorremos atribuindo as posições e colocando no banco, se não tiver, é criado um novo, senão é atribuido
            question = session.exec(
                select(Question).where(
                    Question.exercise_id == exercise.id,
                    Question.position == position,
                )
            ).first()
            if question is None:
                session.add(
                    Question(exercise_id=exercise.id, position=position, text=text)
                )
            else:
                question.text = text


def main():
    create_db_and_tables()
    content = json.loads(SEED_FILE.read_text(encoding="utf-8"))

    with Session(engine) as session:
        seed_encouragements(session, content["encouragements"])
        seed_exercises(session, content["exercises"])
        session.commit()

    print("Carga concluída.")

    if __name__ == "__main__":
        main()
