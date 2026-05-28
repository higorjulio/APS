from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Enrollment, Student, Discipline
from app.schemas import EnrollmentCreate, EnrollmentResponse
from app.auth import get_usuario_atual, apenas_admin

router = APIRouter(prefix="/matriculas", tags=["Matrículas"])

@router.post("/", response_model=EnrollmentResponse, status_code=201)
def criar_matricula(dados: EnrollmentCreate, db: Session = Depends(get_db), usuario = Depends(apenas_admin)):
    if not db.query(Student).filter(Student.id == dados.aluno_id).first():
        raise HTTPException(status_code=404, detail="Aluno não encontrado")

    if not db.query(Discipline).filter(Discipline.id == dados.disciplina_id).first():
        raise HTTPException(status_code=404, detail="Disciplina não encontrada")

    duplicado = db.query(Enrollment).filter(
        Enrollment.aluno_id == dados.aluno_id,
        Enrollment.disciplina_id == dados.disciplina_id,
        Enrollment.semestre == dados.semestre,
        Enrollment.ano == dados.ano
    ).first()
    if duplicado:
        raise HTTPException(status_code=400, detail="Aluno já matriculado nessa disciplina")

    matricula = Enrollment(**dados.model_dump())
    db.add(matricula)
    db.commit()
    db.refresh(matricula)
    return matricula

@router.get("/", response_model=list[EnrollmentResponse])
def listar_matriculas(db: Session = Depends(get_db), usuario = Depends(get_usuario_atual)):
    return db.query(Enrollment).all()

@router.get("/aluno/{aluno_id}", response_model=list[EnrollmentResponse])
def matriculas_do_aluno(aluno_id: int, db: Session = Depends(get_db), usuario = Depends(get_usuario_atual)):
    return db.query(Enrollment).filter(Enrollment.aluno_id == aluno_id).all()

@router.put("/{id}/status", response_model=EnrollmentResponse)
def atualizar_status(id: int, status: str, db: Session = Depends(get_db), usuario = Depends(apenas_admin)):
    if status not in ["ativo", "trancado", "concluido"]:
        raise HTTPException(status_code=400, detail="Status inválido. Use: ativo, trancado, concluido")

    matricula = db.query(Enrollment).filter(Enrollment.id == id).first()
    if not matricula:
        raise HTTPException(status_code=404, detail="Matrícula não encontrada")

    matricula.status = status
    db.commit()
    db.refresh(matricula)
    return matricula

@router.delete("/{id}", status_code=204)
def deletar_matricula(id: int, db: Session = Depends(get_db), usuario = Depends(apenas_admin)):
    matricula = db.query(Enrollment).filter(Enrollment.id == id).first()
    if not matricula:
        raise HTTPException(status_code=404, detail="Matrícula não encontrada")

    db.delete(matricula)
    db.commit()