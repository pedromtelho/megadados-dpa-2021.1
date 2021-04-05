from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, models, schemas
from ..database import SessionLocal

subjectsRouter = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@subjectsRouter.post("/subject", response_model=schemas.Subject)
def create_subject(subject: schemas.SubjectCreate, student_name: str, db: Session = Depends(get_db)):
    db_student = crud.get_user_by_name(db, nome=student_name)
    if db_student:
        db_subject = crud.get_subject_by_name_per_student(
            db, nome=subject.nome, student_id=db_student.id)
        if db_subject:
            raise HTTPException(
                status_code=400, detail="Esta matéria já está cadastrada")
        else:
            return crud.create_subject(db=db, subject=subject, student_id=db_student.id)
    else:
        raise HTTPException(
            status_code=400, detail="Este aluno não está cadastrado")


@subjectsRouter.delete("/subject", response_model=str)
def delete_subject(subject_name: str, student_name: str, db: Session = Depends(get_db)):
    db_student = crud.get_user_by_name(db, nome=student_name)
    if db_student:
        db_subject = crud.get_subject_by_name_per_student(
            db, nome=subject_name, student_id=db_student.id)
        if db_subject:
            return crud.delete_subject(db=db, subject=db_subject)
        else:
            raise HTTPException(
                status_code=400, detail="Esta matéria não existe no banco de dados")
    else:
        raise HTTPException(
            status_code=400, detail="Este aluno não está cadastrado")


@subjectsRouter.get("/subject/user", response_model=[])
def get_students_subjects(student_name: str, db: Session = Depends(get_db)):
    db_student = crud.get_user_by_name(db, nome=student_name)
    if db_student:
        return crud.get_all_subjects_by_user(db=db, student_id=db_student.id)
    else:
        raise HTTPException(
            status_code=400, detail="Este aluno não está cadastrado")


@subjectsRouter.patch("/subject", response_model=str)
def update_subject(subject: schemas.SubjectCreate, subject_name: str, student_name: str, db: Session = Depends(get_db)):
    std = crud.get_user_by_name(db, nome=student_name)
    db_student = crud.get_subject_by_name_per_student(db, nome=subject_name, student_id=std.id)
    if db_student:
        return crud.update_subject(db=db, subject_name=subject_name, subject=subject, student_id=db_student.id)
    else:
        raise HTTPException(
            status_code=400, detail="Aluno ou matéria não estão cadastrados")
