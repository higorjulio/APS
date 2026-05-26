from fastapi import FastAPI
from app.database import Base, engine
import app.models
from app.routes import auth

Base.metadata.create_all(bind=engine)

app = FastAPI(title="SYNCAMPUS")

app.include_router(auth.router)

@app.get("/")
def home():
    return {"message": "SYNCAMPUS rodando"}