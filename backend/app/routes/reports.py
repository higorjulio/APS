from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Student, Discipline, Enrollment, Grade
from app.auth import get_usuario_atual, apenas_admin

router = APIRouter(prefix="/relatorios", tags=["Relatórios"])

@router.get("/dashboard")
def dashboard(db: Session = Depends(get_db), usuario = Depends(apenas_admin)):
    total_alunos = db.query(Student).count()
    total_disciplinas = db.query(Discipline).count()
    total_matriculas = db.query(Enrollment).count()

    notas = db.query(Grade).all()
    aprovados = len([n for n in notas if n.valor >= 7])
    reprovados = len([n for n in notas if n.valor < 7])
    media_geral = round(sum(n.valor for n in notas) / len(notas), 2) if notas else 0

    return {
        "total_alunos": total_alunos,
        "total_disciplinas": total_disciplinas,
        "total_matriculas": total_matriculas,
        "aprovados": aprovados,
        "reprovados": reprovados,
        "media_geral": media_geral
    }

@router.get("/aluno/{aluno_id}")
def relatorio_aluno(aluno_id: int, db: Session = Depends(get_db), usuario = Depends(get_usuario_atual)):
    matriculas = db.query(Enrollment).filter(Enrollment.aluno_id == aluno_id).all()

    resultado = []
    for m in matriculas:
        notas = db.query(Grade).filter(Grade.enrollment_id == m.id).all()
        media = round(sum(n.valor for n in notas) / len(notas), 2) if notas else None
        resultado.append({
            "disciplina_id": m.disciplina_id,
            "semestre": m.semestre,
            "ano": m.ano,
            "status_matricula": m.status,
            "media": media,
            "situacao": "aprovado" if media and media >= 7 else ("reprovado" if media else "sem nota")
        })

    return {"aluno_id": aluno_id, "disciplinas": resultado}

@router.get("/disciplina/{disciplina_id}")
def relatorio_disciplina(disciplina_id: int, db: Session = Depends(get_db), usuario = Depends(get_usuario_atual)):
    matriculas = db.query(Enrollment).filter(Enrollment.disciplina_id == disciplina_id).all()

    resultado = []
    for m in matriculas:
        notas = db.query(Grade).filter(Grade.enrollment_id == m.id).all()
        media = round(sum(n.valor for n in notas) / len(notas), 2) if notas else None
        resultado.append({
            "aluno_id": m.aluno_id,
            "media": media,
            "situacao": "aprovado" if media and media >= 7 else ("reprovado" if media else "sem nota")
        })

    aprovados = len([r for r in resultado if r["situacao"] == "aprovado"])
    reprovados = len([r for r in resultado if r["situacao"] == "reprovado"])

    return {
        "disciplina_id": disciplina_id,
        "total_alunos": len(resultado),
        "aprovados": aprovados,
        "reprovados": reprovados,
        "alunos": resultado
    }