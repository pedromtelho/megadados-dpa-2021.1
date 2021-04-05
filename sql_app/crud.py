from sqlalchemy.orm import Session
from . import models, schemas


# READ

# ----- USER ------
def get_students(db: Session):
    return db.query(models.Student).all()


def get_user_by_name(db: Session, nome: str):
    return db.query(models.Student).filter(models.Student.nome == nome).first()


# ----- SUBJECT ------
def get_subject(db: Session, subject_id: int):
    return db.query(models.Subject).filter(models.Subject.id == subject_id).first()


def get_subject_by_name_per_student(db: Session, nome: str, student_id: int):
    return db.query(models.Subject).filter(models.Subject.nome == nome).first()


def get_all_subjects_by_user(db: Session, skip: int = 0, student_id=int):
    return db.query(models.Subject).filter(models.Subject.id_aluno == student_id).offset(skip).all()


# ----- GRADE ------
def get_grade(db: Session, grade_name: str):
    return db.query(models.Grades).filter(models.Grades.nota == grade_name).first()


def get_grade_by_name(db: Session, name: str):
    return db.query(models.Grades).filter(models.Grades.nota == name).first()


def get_all_grades(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Grades).offset(skip).limit(limit).all()


def get_all_grades_by_subject(db: Session, skip: int = 0, subject_id=int):
    return db.query(models.Grades).filter(models.Grades.id_disciplina == subject_id).offset(skip).all()


# CREATE

# ---- USER -----


def create_student(db: Session, student: schemas.StudentCreate):
    db_student = models.Student(nome=student.nome)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


# ---- SUBJECT -----
def create_subject(db: Session, subject: schemas.SubjectCreate, student_id: int):
    db_subject = models.Subject(**subject.dict(), id_aluno=student_id)
    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)
    return db_subject


# ---- GRADE -----
def create_grade(db: Session, grade: schemas.GradeCreate, subject_id: int):
    db_grade = models.Grades(**grade.dict(), id_disciplina=subject_id)
    db.add(db_grade)
    db.commit()
    db.refresh(db_grade)
    return db_grade


# DELETE

# ---- SUBJECT -----
def delete_subject(db: Session,  subject: schemas.Subject):
    db.delete(subject)
    db.commit()
    return "Matéria excluída com sucesso"

# ---- GRADE -----


def delete_grade(db: Session,  grade: schemas.Grade):
    db.delete(grade)
    db.commit()
    return "Nota excluída com sucesso"


# UPDATE


# ---- SUBJECT -----
def update_subject(db: Session, subject_name: str, subject: schemas.SubjectCreate, student_id: int):
    db.query(models.Subject).filter(
        models.Subject.nome == subject_name).update({models.Subject.nome: subject.nome, models.Subject.professor: subject.professor,
                                                     models.Subject.campo: subject.campo})
    # new_subject = models.Subject(
    #     **subject.dict(), id_aluno=student_id, id=old_subject.id)
    db.commit()
    return "Updated successfully!"


# ---- GRADE -----
def create_grade(db: Session, grade: schemas.GradeCreate, subject_id: int):
    db_grade = models.Grades(**grade.dict(), id_disciplina=subject_id)
    db.add(db_grade)
    db.commit()
    return db_grade


def update_grade(db: Session, name: str, new_grade: schemas.GradeCreate):
    db.query(models.Grades).filter(models.Grades.nota == name).update(
        {models.Grades.nota: new_grade.nota, models.Grades.valor: new_grade.valor})
    db.commit()
    return "Updated successfully!"
