"""
Módulo del repositorio de chat.
Implementa el acceso a datos del historial de conversaciones usando SQLAlchemy.
"""

from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from src.domain.entities import ChatMessage
from src.domain.repositories import IChatRepository
from src.infrastructure.db.models import ChatMemoryModel


class SQLChatRepository(IChatRepository):
    """
    Implementación del repositorio de chat usando SQLAlchemy.
    
    Gestiona el acceso a la tabla chat_memory en la base de datos,
    convirtiendo entre modelos ORM y entidades del dominio.
    
    Attributes:
        db (Session): Sesión de base de datos de SQLAlchemy.
    """

    def __init__(self, db: Session):
        """
        Inicializa el repositorio con una sesión de base de datos.
        
        Args:
            db (Session): Sesión activa de SQLAlchemy.
        """
        self.db = db

    def save_message(self, message: ChatMessage) -> ChatMessage:
        """
        Guarda un mensaje en el historial de conversación.
        
        Args:
            message (ChatMessage): Mensaje a guardar.
        
        Returns:
            ChatMessage: El mensaje guardado con su ID asignado.
        """
        model = self._entity_to_model(message)
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return self._model_to_entity(model)

    def get_session_history(self, session_id: str, limit: Optional[int] = None) -> List[ChatMessage]:
        """
        Obtiene el historial completo de una sesión de chat.
        
        Args:
            session_id (str): Identificador de la sesión.
            limit (Optional[int]): Número máximo de mensajes a retornar.
        
        Returns:
            List[ChatMessage]: Lista de mensajes en orden cronológico.
        """
        query = self.db.query(ChatMemoryModel).filter(
            ChatMemoryModel.session_id == session_id
        ).order_by(ChatMemoryModel.timestamp.asc())

        if limit:
            query = query.limit(limit)

        return [self._model_to_entity(m) for m in query.all()]

    def delete_session_history(self, session_id: str) -> int:
        """
        Elimina todo el historial de una sesión de chat.
        
        Args:
            session_id (str): Identificador de la sesión a eliminar.
        
        Returns:
            int: Cantidad de mensajes eliminados.
        """
        count = self.db.query(ChatMemoryModel).filter(
            ChatMemoryModel.session_id == session_id
        ).count()
        self.db.query(ChatMemoryModel).filter(
            ChatMemoryModel.session_id == session_id
        ).delete()
        self.db.commit()
        return count

    def get_recent_messages(self, session_id: str, count: int) -> List[ChatMessage]:
        """
        Obtiene los últimos N mensajes de una sesión en orden cronológico.
        
        Args:
            session_id (str): Identificador de la sesión.
            count (int): Número de mensajes a retornar.
        
        Returns:
            List[ChatMessage]: Lista de mensajes en orden cronológico.
        """
        models = self.db.query(ChatMemoryModel).filter(
            ChatMemoryModel.session_id == session_id
        ).order_by(ChatMemoryModel.timestamp.desc()).limit(count).all()

        models.reverse()
        return [self._model_to_entity(m) for m in models]

    def _model_to_entity(self, model: ChatMemoryModel) -> ChatMessage:
        """
        Convierte un modelo ORM a una entidad del dominio.
        
        Args:
            model (ChatMemoryModel): Modelo ORM a convertir.
        
        Returns:
            ChatMessage: Entidad del dominio correspondiente.
        """
        return ChatMessage(
            id=model.id,
            session_id=model.session_id,
            role=model.role,
            message=model.message,
            timestamp=model.timestamp
        )

    def _entity_to_model(self, message: ChatMessage) -> ChatMemoryModel:
        """
        Convierte una entidad del dominio a un modelo ORM.
        
        Args:
            message (ChatMessage): Entidad a convertir.
        
        Returns:
            ChatMemoryModel: Modelo ORM correspondiente.
        """
        return ChatMemoryModel(
            session_id=message.session_id,
            role=message.role,
            message=message.message,
            timestamp=message.timestamp
        )