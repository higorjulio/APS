from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserLogin, UserResponse, Token
from app.auth import hash_senha, verificar_senha, criar_token, get_usuario_atual

router = APIRouter(prefix="/auth", tags=["Autenticação"])

@router.post("/register", response_model=UserResponse, status_code=201)
def registrar(dados: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == dados.email).first():
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")

    usuario = User(
        name=dados.name,
        email=dados.email,
        password=hash_senha(dados.password),
        role=dados.role
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario

@router.post("/login", response_model=Token)
def login(dados: UserLogin, db: Session = Depends(get_db)):
    usuario = db.query(User).filter(User.email == dados.email).first()
    if not usuario or not verificar_senha(dados.password, usuario.password):
        raise HTTPException(status_code=401, detail="E-mail ou senha incorretos")

    token = criar_token({"sub": usuario.email, "role": usuario.role})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
def meu_perfil(usuario: User = Depends(get_usuario_atual)):
    return usuario