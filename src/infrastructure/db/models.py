"""
Módulo de modelos ORM.
Define los modelos de SQLAlchemy que mapean las tablas de la base de datos.
"""

from sqlalchemy import Column, Integer, String, Float, Text, DateTime, Index
from datetime import datetime
from src.infrastructure.db.database import Base


class ProductModel(Base):
    """
    Modelo ORM que representa la tabla de productos.
    
    Mapea la tabla 'products' en la base de datos SQLite
    con todos los atributos de un zapato.
    """
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    brand = Column(String(100))
    category = Column(String(100))
    size = Column(String(20))
    color = Column(String(50))
    price = Column(Float)
    stock = Column(Integer)
    description = Column(Text)


class ChatMemoryModel(Base):
    """
    Modelo ORM que representa la tabla de historial de chat.
    
    Mapea la tabla 'chat_memory' en la base de datos SQLite,
    almacenando cada mensaje de las conversaciones con la IA.
    """
    __tablename__ = "chat_memory"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(100), index=True)
    role = Column(String(20))
    message = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)