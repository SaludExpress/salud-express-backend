from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Configuración de la Base de Datos
DATABASE_URL = os.getenv("DATABASE_URL") 
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modelo de Datos (Cómo se guarda el paciente)
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    edad = Column(Integer)
    sexo = Column(String)
    telefono = Column(String)
    empresa = Column(String)
    tiene_seguro = Column(Boolean)
    alergias = Column(Text)
    cronicas = Column(Text)
    medicamentos = Column(Text)
    molestias = Column(Text)

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Permitir que la app de CodeSandbox se conecte al servidor
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

# Esquema para recibir datos
class UserCreate(BaseModel):
    nombre: str
    edad: int
    sexo: str
    telefono: str
    empresa: str
    tieneSeguro: bool
    alergias: str
    cronicas: str
    medicamentos: str
    molestias: str

@app.get("/")
def read_root():
    return {"status": "Salud Express Backend Activo"}

@app.post("/register")
def register_user(user: UserCreate):
    try:
        db = SessionLocal()
        db_user = User(
            nombre=user.nombre, edad=user.edad, sexo=user.sexo,
            telefono=user.telefono, empresa=user.empresa, 
            tiene_seguro=user.tieneSeguro, alergias=user.alergias,
            cronicas=user.cronicas, medicamentos=user.medicamentos,
            molestias=user.molestias
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        db.close()
        return {"message": "Paciente registrado con éxito", "id": db_user.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
