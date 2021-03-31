from sqlalchemy.orm import Session
from . import models, schemas


# READ
def get_student(db: Session, student_id: int):
    return db.query(models.Student).filter(models.Student.id == student_id).first()


def get_user_by_name(db: Session, nome: str):
    return db.query(models.Student).filter(models.Student.nome == nome).first()


def get_subject(db: Session, subject_id: int):
    return db.query(models.Subject).filter(models.Subject.id == subject_id).first()


def get_grade(db: Session, grade_id: int):
    return db.query(models.Grades).filter(models.Grades.id == grade_id).first()


def get_all_subjects(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Subject).offset(skip).limit(limit).all()


def get_all_grades(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Grades).offset(skip).limit(limit).all()

# CREATE


def create_student(db: Session, student: schemas.StudentCreate):
    db_student = models.Student(nome=student.nome)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


def create_subject(db: Session, subject: schemas.SubjectCreate, student_id: int):
    db_subject = models.Subject(**subject.dict(), id_aluno=student_id)
    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)
    return db_subject


def create_grade(db: Session, grade: schemas.GradeCreate, subject_id: int):
    db_grade = models.Grades(**grade.dict(), id_disciplina=subject_id)
    db.add(db_grade)
    db.commit()
    db.refresh(db_grade)
    return db_grade
