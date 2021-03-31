from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, models, schemas
from ..database import SessionLocal

studentsRouter = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@studentsRouter.post("/students", response_model=schemas.Student)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    db_student = crud.get_user_by_name(db, nome=student.nome)
    if db_student:
        raise HTTPException(status_code=400, detail="Este aluno já existe")
    return crud.create_student(db=db, student=student)
