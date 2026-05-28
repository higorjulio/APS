from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Grade, Enrollment
from app.schemas import GradeCreate, GradeResponse
from app.auth import get_usuario_atual, apenas_admin

router = APIRouter(prefix="/notas", tags=["Notas"])

@router.post("/", response_model=GradeResponse, status_code=201)
def lancar_nota(dados: GradeCreate, db: Session = Depends(get_db), usuario = Depends(get_usuario_atual)):
    if usuario.role not in ["admin", "professor"]:
        raise HTTPException(status_code=403, detail="Apenas admin ou professor podem lançar notas")

    if not db.query(Enrollment).filter(Enrollment.id == dados.enrollment_id).first():
        raise HTTPException(status_code=404, detail="Matrícula não encontrada")

    nota = Grade(**dados.model_dump())
    db.add(nota)
    db.commit()
    db.refresh(nota)
    return nota

@router.get("/matricula/{enrollment_id}", response_model=list[GradeResponse])
def notas_da_matricula(enrollment_id: int, db: Session = Depends(get_db), usuario = Depends(get_usuario_atual)):
    return db.query(Grade).filter(Grade.enrollment_id == enrollment_id).all()

@router.put("/{id}", response_model=GradeResponse)
def atualizar_nota(id: int, dados: GradeCreate, db: Session = Depends(get_db), usuario = Depends(get_usuario_atual)):
    if usuario.role not in ["admin", "professor"]:
        raise HTTPException(status_code=403, detail="Apenas admin ou professor podem editar notas")

    nota = db.query(Grade).filter(Grade.id == id).first()
    if not nota:
        raise HTTPException(status_code=404, detail="Nota não encontrada")

    nota.atividade = dados.atividade
    nota.valor = dados.valor
    db.commit()
    db.refresh(nota)
    return nota

@router.delete("/{id}", status_code=204)
def deletar_nota(id: int, db: Session = Depends(get_db), usuario = Depends(apenas_admin)):
    nota = db.query(Grade).filter(Grade.id == id).first()
    if not nota:
        raise HTTPException(status_code=404, detail="Nota não encontrada")

    db.delete(nota)
    db.commit()