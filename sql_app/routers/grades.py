from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, models, schemas
from ..database import SessionLocal

gradesRouter = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@gradesRouter.post("/grades", response_model=schemas.Grade)
def create_grade(grade: schemas.GradeCreate, subject_name: str, student_name: str, db: Session = Depends(get_db)):
    db_student = crud.get_user_by_name(db, nome=student_name)
    if db_student:
        db_subject = crud.get_subject_by_name_per_student(
            db, nome=subject_name, student_id=db_student.id)
        if db_subject:
            return crud.create_grade(db=db, grade=grade, subject_id=db_subject.id)
        else:
            raise HTTPException(
                status_code=400, detail="Esta matéria não existe")
    else:
        raise HTTPException(status_code=400, detail="Este aluno não existe")


@gradesRouter.delete("/grades", response_model=str)
def delete_grade(subject_name: str, student_name: str, grade_name: str, db: Session = Depends(get_db)):
    db_student = crud.get_user_by_name(db, nome=student_name)
    if db_student:
        db_subject = crud.get_subject_by_name_per_student(
            db, nome=subject_name, student_id=db_student.id)
        if db_subject:
            db_grade = crud.get_grade(db=db, grade_name=grade_name)
            if db_grade:
                return crud.delete_grade(db=db, grade=db_grade)
            else:
                raise HTTPException(
                    status_code=400, detail="Esta nota não existe no banco de dados")
        else:
            raise HTTPException(
                status_code=400, detail="Esta matéria não existe no banco de dados")
    else:
        raise HTTPException(
            status_code=400, detail="Este aluno não está cadastrado")


@gradesRouter.get("/grades/subject", response_model=[])
def get_subjects_grades(student_name: str, subject_name: str, db: Session = Depends(get_db)):
    db_student = crud.get_user_by_name(db, nome=student_name)
    if db_student:
        db_subject = crud.get_subject_by_name_per_student(
            db=db, nome=subject_name, student_id=db_student.id)
        if db_subject:
            return crud.get_all_grades_by_subject(db=db, subject_id=db_subject.id)
        else:
            raise HTTPException(
                status_code=400, detail="Esta matéria não existe")
    else:
        raise HTTPException(
            status_code=400, detail="Este aluno não está cadastrado")

@gradesRouter.patch("/grades", response_model=str)
def update_grade(grade: schemas.GradeCreate, subject_name: str, student_name: str, grade_id: int, db: Session = Depends(get_db)):
    db_student = crud.get_user_by_name(db, nome=student_name)
    if db_student:
        db_subject = crud.get_subject_by_name_per_student(
            db, nome=subject_name, student_id=db_student.id)
        if db_subject:
            db_grade = crud.get_grade_by_id(db=db, id=grade_id)
            if db_grade:
                return crud.update_grade(db=db, new_grade=grade, id=grade_id)
            else:
                raise HTTPException(
                    status_code=400, detail="Esta nota não existe no banco de dados")
        else:
            raise HTTPException(
                status_code=400, detail="Esta matéria não existe no banco de dados")
    else:
        raise HTTPException(
            status_code=400, detail="Este aluno não está cadastrado")

