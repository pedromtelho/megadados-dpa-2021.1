from typing import List, Optional
from pydantic import BaseModel


# Lidando com o dado do tipo Subject

class SubjectBase(BaseModel):
    nome: str
    campo: Optional[str] = None
    professor: Optional[str] = None


class SubjectCreate(SubjectBase):
    pass


class Subject(SubjectBase):
    id: int
    id_aluno: int

    class Config:
        orm_mode = True


# Lidando com o dado do tipo Student


class StudentBase(BaseModel):
    nome: str


class StudentCreate(StudentBase):
    pass


class Student(StudentBase):
    id: int

    class Config:
        orm_mode = True


# Lidando com o dado do tipo Grade


class GradeBase(BaseModel):
    nota: str
    valor: float


class GradeCreate(GradeBase):
    pass


class Grade(GradeBase):
    id: int
    id_disciplina: int

    class Config:
        orm_mode = True
