from fastapi import FastAPI
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Dict, List

app = FastAPI()

disciplinas = {"nome": [], "id": [],
               "id_aluno": [], "campo": [], "professor": []}
alunos = {"id": [], "nome": []}
notas = {"id": [], "id_disciplina": [], "nota": [], "valor": []}


class Disciplina(BaseModel):
    id: int
    nome: str
    campo: Optional[str]
    id_aluno: int
    professor: Optional[str]


class DisciplinaEdit(BaseModel):
    nome: Optional[str]
    campo: Optional[str]
    professor: Optional[str]


class Nota(BaseModel):
    id: int
    id_disciplina: int
    nota: str
    valor: float


class NotaEdit(BaseModel):
    nota: Optional[str]
    valor: Optional[float]


class Aluno(BaseModel):
    id: int
    nome: str


@app.post("/student", response_model=Aluno)
async def create_student(aluno: Aluno):
    if aluno.id not in alunos["id"]:
        alunos["id"].append(aluno.id)
        alunos["nome"].append(aluno.nome)
    else:
        raise Exception("Id de aluno já existe")
    return {"id": aluno.id, "nome": aluno.nome}


@app.post("/subject", response_model=Disciplina)
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


@app.delete("/subject", response_model=str)
async def delete_subject(id_disciplina: int):
    if (id_disciplina in disciplinas["id"]):
        if(id_disciplina in notas["id_disciplina"]):
            for i in range(0, len(notas["id_disciplina"])):
                if id_disciplina == notas["id_disciplina"][i]:
                    idx = notas["id_disciplina"].index(id_disciplina)
                    del notas["id"][idx]
                    del notas["id_disciplina"][idx]
                    del notas["nota"][idx]
                    del notas["valor"][idx]
        idx = disciplinas["id"].index(id_disciplina)
        del disciplinas["id"][idx]
        del disciplinas["nome"][idx]
        del disciplinas["id_aluno"][idx]
        del disciplinas["campo"][idx]
        del disciplinas["professor"][idx]
    else:
        raise Exception("Disciplina inexistente")

    return "Disciplina deletada com sucesso"


@app.patch("/subject", response_model=str)
async def edit_subject(id_disciplina: int, disciplina: DisciplinaEdit):
    if id_disciplina in disciplinas["id"] and (disciplina.nome not in disciplinas["nome"]):
        idx = disciplinas["id"].index(id_disciplina)
        disciplinas["nome"][idx] = disciplina.nome
        disciplinas["campo"][idx] = disciplina.campo
        disciplinas["professor"][idx] = disciplina.professor
    else:
        raise Exception("Id disciplina inexistente ou novo nome já existe")
    return "Disciplina editada com sucesso"


@app.post("/grade", response_model=Nota)
async def create_grade(nota: Nota):
    if (nota.id_disciplina in disciplinas["id"]) and (nota.id not in notas["id"]):
        notas["id"].append(nota.id)
        notas["nota"].append(nota.nota)
        notas["valor"].append(nota.valor)
        notas["id_disciplina"].append(nota.id_disciplina)
    else:
        raise Exception("Disciplina não existe ou ID da nota já existente")

    return {"id": nota.id, "nota": nota.nota, "valor": nota.valor, "id_disciplina": nota.id_disciplina}


@app.delete("/grade", response_model=str)
async def delete_grade(id_nota: int):
    if (id_nota in notas["id"]):
        idx = notas["id"].index(id_nota)
        del notas["id"][idx]
        del notas["id_disciplina"][idx]
        del notas["nota"][idx]
        del notas["valor"][idx]
    else:
        raise Exception("Nota inexistente")
    return "Nota deletada com sucesso"


@app.patch("/grade", response_model=str)
async def edit_grade(id_nota: int, nota: NotaEdit):
    if id_nota in notas["id"]:
        idx = notas["id"].index(id_nota)
        notas["nota"][idx] = nota.nota
        notas["valor"][idx] = nota.valor
    else:
        raise Exception("Nota inexistente")
    return "Nota editada com sucesso"


@app.get("/subjects", response_model=List[dict])
async def list_subjects(id_aluno: int):
    aluno_disciplinas = []
    if id_aluno in alunos["id"]:
        for i in range(0, len(disciplinas["id_aluno"])):
            if disciplinas["id_aluno"][i] == id_aluno:
                objetos_disciplinas = {
                    "id": "", "nome": "", "professor": "", "campo": ""}
                objetos_disciplinas["id"] = disciplinas["id"][i]
                objetos_disciplinas["nome"] = disciplinas["nome"][i]
                objetos_disciplinas["professor"] = disciplinas["professor"][i]
                objetos_disciplinas["campo"] = disciplinas["campo"][i]
                aluno_disciplinas.append(objetos_disciplinas)
        return aluno_disciplinas
    else:
        raise Exception("Aluno inexistente")


@app.get("/grades", response_model=List[dict])
async def list_grades(id_disciplina: int):
    notas_disciplinas = []
    if id_disciplina in disciplinas["id"]:
        for i in range(0, len(notas["id_disciplina"])):
            if notas["id_disciplina"][i] == id_disciplina:
                objetos_nota = {"id": "", "nota": "", "valor": ""}
                objetos_nota["id"] = notas["id"][i]
                objetos_nota["nota"] = notas["nota"][i]
                objetos_nota["valor"] = notas["valor"][i]
                notas_disciplinas.append(objetos_nota)
        return notas_disciplinas
    else:
        raise Exception("Disciplina inexistente")
