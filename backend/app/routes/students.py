from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Student, User
from app.schemas import StudentCreate, StudentResponse
from app.auth import get_usuario_atual, apenas_admin
import datetime

router = APIRouter(prefix="/alunos", tags=["Alunos"])

def gerar_matricula(db: Session):
    ano = datetime.datetime.now().year
    total = db.query(Student).count() + 1
    return f"{ano}{total:04d}"

#CRIAR ALUNO

@router.post("/", response_model=StudentResponse, status_code=201)
def criar_aluno(dados: StudentCreate, db: Session = Depends(get_db), usuario = Depends(apenas_admin)):
    if not db.query(User).filter(User.id == dados.user_id).first():
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    if db.query(Student).filter(Student.user_id == dados.user_id).first():
        raise HTTPException(status_code=400, detail="Usuário já possui perfil de aluno")

    aluno = Student(
        user_id=dados.user_id,
        matricula=gerar_matricula(db),
        curso=dados.curso,
        semestre=dados.semestre
    )
    db.add(aluno)
    db.commit()
    db.refresh(aluno)
    return aluno

#LISTAR ALUNOS

@router.get("/", response_model=list[StudentResponse])
def listar_alunos(db: Session = Depends(get_db), usuario = Depends(get_usuario_atual)):
    return db.query(Student).all()

#BUSCAR ALUNOS

@router.get("/buscar", response_model=list[StudentResponse])
def buscar_alunos(q: str, db: Session = Depends(get_db), usuario = Depends(get_usuario_atual)):
    return db.query(Student).filter(
        Student.matricula.contains(q) | Student.curso.contains(q)
    ).all()

#BUSCAR ALUNO POR ID

@router.get("/{id}", response_model=StudentResponse)
def buscar_aluno(id: int, db: Session = Depends(get_db), usuario = Depends(get_usuario_atual)):
    aluno = db.query(Student).filter(Student.id == id).first()
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return aluno

#ATUALIZAR ALUNO

@router.put("/{id}", response_model=StudentResponse)
def atualizar_aluno(id: int, dados: StudentCreate, db: Session = Depends(get_db), usuario = Depends(apenas_admin)):
    aluno = db.query(Student).filter(Student.id == id).first()
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")

    aluno.curso = dados.curso
    aluno.semestre = dados.semestre
    db.commit()
    db.refresh(aluno)
    return aluno

#DELETAR ALUNO

@router.delete("/{id}", status_code=204)
def deletar_aluno(id: int, db: Session = Depends(get_db), usuario = Depends(apenas_admin)):
    aluno = db.query(Student).filter(Student.id == id).first()
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")

    db.delete(aluno)
    db.commit()