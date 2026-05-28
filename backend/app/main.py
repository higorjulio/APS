from fastapi import FastAPI
from app.database import Base, engine
import app.models
from app.routes import auth, students, disciplines, enrollments, grades, reports

Base.metadata.create_all(bind=engine)

app = FastAPI(title="SynCampus")

app.include_router(auth.router)
app.include_router(students.router)
app.include_router(disciplines.router)
app.include_router(enrollments.router)
app.include_router(grades.router)
app.include_router(reports.router)

@app.get("/")
def home():
    return {"mensagem": "API SynCampus rodando!"}