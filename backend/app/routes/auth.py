from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, Student
from app.schemas import UserCreate, UserLogin, UserResponse, Token
from app.auth import hash_senha, verificar_senha, criar_token, get_usuario_atual
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/auth", tags=["Autenticação"])

#REGISTRAR

@router.post("/register", response_model=UserResponse, status_code=201)
def registrar(dados: UserCreate, db: Session = Depends(get_db)):
    try:
        # Validar email duplicado
        if db.query(User).filter(User.email == dados.email).first():
            raise HTTPException(status_code=400, detail="E-mail já cadastrado")
        
        # Validar role
        if dados.role not in ["aluno", "professor", "admin"]:
            raise HTTPException(status_code=400, detail="role inválido")
        
        # Hash da senha
        try:
            senha_hash = hash_senha(dados.password)
        except Exception as e:
            logger.error(f"Erro ao fazer hash da senha: {str(e)}")
            raise HTTPException(status_code=500, detail="Erro ao processar senha")
        
        # Criar usuário
        usuario = User(
            name=dados.name,
            email=dados.email,
            password=senha_hash,
            role=dados.role
        )
        db.add(usuario)
        db.commit()
        db.refresh(usuario)
        
        # Se for aluno, criar registro em Student
        if dados.role == "aluno":
            try:
                aluno = Student(
                    user_id=usuario.id,
                    matricula=f"ALU{usuario.id:06d}",
                    curso="Não definido",
                    semestre=1
                )
                db.add(aluno)
                db.commit()
            except Exception as e:
                logger.error(f"Erro ao criar aluno: {str(e)}")
                db.rollback()
                # Não falha o registro, só não cria aluno
        
        return usuario
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro no registro: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Erro ao registrar usuário")

#LOGIN

@router.post("/login", response_model=Token)
def login(dados: UserLogin, db: Session = Depends(get_db)):
    usuario = db.query(User).filter(User.email == dados.email).first()
    if not usuario or not verificar_senha(dados.password, usuario.password):
        raise HTTPException(status_code=401, detail="E-mail ou senha incorretos")

    token = criar_token({"sub": usuario.email, "role": usuario.role})
    return {"access_token": token, "token_type": "bearer"}

#PERFIL DO USER

@router.get("/me", response_model=UserResponse)
def meu_perfil(usuario: User = Depends(get_usuario_atual)):
    return usuario

# INSOMNIA:
# usa o get, vai em header e adiciona Authorization | Bearer token_login