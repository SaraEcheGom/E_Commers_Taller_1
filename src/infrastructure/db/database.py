"""
Módulo de configuración de la base de datos.
Configura SQLAlchemy y provee la sesión de base de datos.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/ecommerce_chat.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """
    Dependency de FastAPI para obtener una sesión de base de datos.
    
    Provee una sesión de base de datos y la cierra automáticamente
    después de cada request usando el patrón yield.
    
    Yields:
        Session: Sesión activa de SQLAlchemy.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Inicializa la base de datos creando todas las tablas.
    
    Crea las tablas definidas en los modelos ORM y carga
    los datos iniciales si la base de datos está vacía.
    """
    from src.infrastructure.db.models import ProductModel, ChatMemoryModel
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        from src.infrastructure.db.init_data import load_initial_data
        load_initial_data(db)
    finally:
        db.close()