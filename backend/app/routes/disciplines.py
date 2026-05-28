from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Discipline, User
from app.schemas import DisciplineCreate, DisciplineResponse
from app.auth import get_usuario_atual, apenas_admin

router = APIRouter(prefix="/disciplinas", tags=["Disciplinas"])

#criar disciplinas

@router.post("/", response_model=DisciplineResponse, status_code=201)
def criar_disciplina(dados: DisciplineCreate, db: Session = Depends(get_db), usuario = Depends(apenas_admin)):
    if db.query(Discipline).filter(Discipline.codigo == dados.codigo).first():
        raise HTTPException(status_code=400, detail="Código já cadastrado")

    if dados.professor_id:
        professor = db.query(User).filter(User.id == dados.professor_id, User.role == "professor").first()
        if not professor:
            raise HTTPException(status_code=404, detail="Professor não encontrado")

    disciplina = Discipline(**dados.model_dump())
    db.add(disciplina)
    db.commit()
    db.refresh(disciplina)
    return disciplina

#listar disciplinas

@router.get("/", response_model=list[DisciplineResponse])
def listar_disciplinas(db: Session = Depends(get_db), usuario = Depends(get_usuario_atual)):
    return db.query(Discipline).all()

#buscar  por nome ou codigo

@router.get("/buscar", response_model=list[DisciplineResponse])
def buscar_disciplinas(q: str, db: Session = Depends(get_db), usuario = Depends(get_usuario_atual)):
    return db.query(Discipline).filter(
        Discipline.nome.contains(q) | Discipline.codigo.contains(q)
    ).all()

#buscar por id

@router.get("/{id}", response_model=DisciplineResponse)
def buscar_disciplina(id: int, db: Session = Depends(get_db), usuario = Depends(get_usuario_atual)):
    disciplina = db.query(Discipline).filter(Discipline.id == id).first()
    if not disciplina:
        raise HTTPException(status_code=404, detail="Disciplina não encontrada")
    return disciplina

#atualizar disciplina

@router.put("/{id}", response_model=DisciplineResponse)
def atualizar_disciplina(id: int, dados: DisciplineCreate, db: Session = Depends(get_db), usuario = Depends(apenas_admin)):
    disciplina = db.query(Discipline).filter(Discipline.id == id).first()
    if not disciplina:
        raise HTTPException(status_code=404, detail="Disciplina não encontrada")

    disciplina.codigo = dados.codigo
    disciplina.nome = dados.nome
    disciplina.professor_id = dados.professor_id
    db.commit()
    db.refresh(disciplina)
    return disciplina

#deletar disciplina

@router.delete("/{id}", status_code=204)
def deletar_disciplina(id: int, db: Session = Depends(get_db), usuario = Depends(apenas_admin)):
    disciplina = db.query(Discipline).filter(Discipline.id == id).first()
    if not disciplina:
        raise HTTPException(status_code=404, detail="Disciplina não encontrada")

    db.delete(disciplina)
    db.commit()