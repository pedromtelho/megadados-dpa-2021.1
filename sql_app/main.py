from fastapi import FastAPI
from . import models
from .database import engine

from .routers.student import studentsRouter
from .routers.subjects import subjectsRouter
from .routers.grades import gradesRouter

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title='Grades Manager',
    description='Manage all your grades by studied subject')

app.include_router(studentsRouter, tags=["Students"])
app.include_router(subjectsRouter, tags=["Subjects"])
app.include_router(gradesRouter, tags=["Grades"])
