from fastapi import FastAPI
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Dict, List

app = FastAPI()

disciplinas = {"nome": [], "id": [], "id_aluno": [], "campo": [], "professor": []}
alunos = {"id": [], "nome": []}
notas = {"id": [], "id_disciplina": [], "nota": [], "valor": []}

class Disciplina(BaseModel):
    id: int
    nome: str
    campo: Optional[str]
    id_aluno: int
    professor: str

class Nota(BaseModel):
    id: int
    id_disciplina: int
    nota: str
    valor: float

class Aluno(BaseModel):
    id: int
    nome: str

@app.post("/api/create_student",response_model=Aluno)
async def create_student(aluno: Aluno):
    try:
        if aluno.id not in alunos["id"]:
            alunos["id"].append(aluno.id)
            alunos["nome"].append(aluno.nome)
    except:
        raise Exception("Id de aluno já existe")
    return {"id": aluno.id, "nome": aluno.nome}

@app.post("/api/create_subject", response_model=Disciplina)
async def create_subject(disciplina: Disciplina):
    if (disciplina.id_aluno in alunos["id"]) and (disciplina.id not in disciplinas["id"]) and (disciplina.nome not in disciplinas["nome"]):
        disciplinas["id"].append(disciplina.id)
        disciplinas["nome"].append(disciplina.nome)
        disciplinas["id_aluno"].append(disciplina.id_aluno)
        disciplinas["campo"].append(disciplina.campo)
        disciplinas["professor"].append(disciplina.professor)
    else:
        raise Exception("Aluno não existe ou disciplina já existente")

    return {"nome": disciplina.nome, "id": disciplina.id, "id_aluno": disciplina.id_aluno, "campo": disciplina.campo, "professor": disciplina.professor}

@app.post("/api/create_grade", response_model=Nota)
async def create_subject(nota: Nota):
    if (nota.id_disciplina in disciplinas["id"]) and (nota.id not in notas["id"]):
        notas["id"].append(nota.id)
        notas["nota"].append(nota.nota)
        notas["valor"].append(nota.valor)
        notas["id_disciplina"].append(nota.id_disciplina)
    else:
        raise Exception("Disciplina não existe ou ID da nota já existente")

    return {"id": nota.id, "nota": nota.nota, "valor": nota.valor, "id_disciplina": nota.id_disciplina}

@app.get("/api/subjects", response_model=List[str])
async def list_subjects(id_aluno: int):
    aluno_disciplinas = []
    for i in range(0, len(disciplinas["id_aluno"])):
        print(disciplinas)
        print(disciplinas["id_aluno"])
        if disciplinas["id_aluno"][i] == id_aluno:
            aluno_disciplinas.append(disciplinas["nome"][i])
    print(aluno_disciplinas)
    return aluno_disciplinas



    