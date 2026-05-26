from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(100), unique=True, index=True)
    password = Column(String(255))
    role = Column(String(20), default="aluno")  # admin, professor, aluno
    ativo = Column(Boolean, default=True)

    aluno = relationship("Student", back_populates="user", uselist=False)


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    matricula = Column(String(20), unique=True)
    curso = Column(String(100))
    semestre = Column(Integer, default=1)

    user = relationship("User", back_populates="aluno")
    matriculas = relationship("Enrollment", back_populates="aluno")


class Discipline(Base):
    __tablename__ = "disciplines"

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(20), unique=True)
    nome = Column(String(100))
    professor_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    matriculas = relationship("Enrollment", back_populates="disciplina")


class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, index=True)
    aluno_id = Column(Integer, ForeignKey("students.id"))
    disciplina_id = Column(Integer, ForeignKey("disciplines.id"))
    semestre = Column(Integer)
    ano = Column(Integer)
    status = Column(String(20), default="ativo")  # ativo, trancado, concluido

    aluno = relationship("Student", back_populates="matriculas")
    disciplina = relationship("Discipline", back_populates="matriculas")
    notas = relationship("Grade", back_populates="matricula")


class Grade(Base):
    __tablename__ = "grades"

    id = Column(Integer, primary_key=True, index=True)
    enrollment_id = Column(Integer, ForeignKey("enrollments.id"))
    atividade = Column(String(100), default="Nota Final")
    valor = Column(Float)

    matricula = relationship("Enrollment", back_populates="notas")