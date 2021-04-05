from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship, backref

from .database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(128), unique=True, index=True)
    subjects = relationship("Subject", cascade="all, delete-orphan")


class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(128), index=True)
    campo = Column(String(128))
    professor = Column(String(128))
    id_aluno = Column(Integer, ForeignKey("students.id"))
    grades = relationship("Grades", cascade="all, delete-orphan")
    student = relationship("Student",
                           backref=backref(
                               "Grades", cascade="all, delete-orphan")
                           )


class Grades(Base):
    __tablename__ = "grades"

    id = Column(Integer, primary_key=True, index=True)
    id_disciplina = Column(Integer, ForeignKey("subjects.id"))
    nota = Column(String(128))
    valor = Column(Float)
    subject = relationship("Subject",
                           backref=backref(
                               "Grades", cascade="all, delete-orphan")
                           )
