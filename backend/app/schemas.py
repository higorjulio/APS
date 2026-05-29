from pydantic import BaseModel, EmailStr
from typing import Optional

# --- Auth ---

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str = "aluno"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# --- Student ---

class StudentCreate(BaseModel):
    user_id: int
    curso: str
    semestre: int = 1

class StudentResponse(BaseModel):
    id: int
    matricula: str
    curso: str
    semestre: int

    class Config:
        from_attributes = True

# --- Discipline ---

class DisciplineCreate(BaseModel):
    codigo: str
    nome: str
    professor_id: Optional[int] = None

class DisciplineResponse(BaseModel):
    id: int
    codigo: str
    nome: str

    class Config:
        from_attributes = True

# --- Enrollment ---

class EnrollmentCreate(BaseModel):
    aluno_id: int
    disciplina_id: int
    semestre: int
    ano: int

class EnrollmentResponse(BaseModel):
    id: int
    aluno_id: int
    disciplina_id: int
    status: str

    class Config:
        from_attributes = True

# --- Grade ---

class GradeCreate(BaseModel):
    enrollment_id: int
    atividade: str = "Nota Final"
    valor: float

class GradeResponse(BaseModel):
    id: int
    enrollment_id: int
    atividade: str
    valor: float

    class Config:
        from_attributes = True