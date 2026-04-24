"""
Módulo del servicio de chat.
Implementa los casos de uso del chat conversacional con IA.
"""

from datetime import datetime
from typing import List, Optional
import traceback
from src.domain.entities import ChatMessage, ChatContext
from src.domain.repositories import IProductRepository, IChatRepository
from src.domain.exceptions import ChatServiceError
from src.application.dtos import ChatMessageRequestDTO, ChatMessageResponseDTO, ChatHistoryDTO


class ChatService:
    """
    Servicio de aplicación para gestionar el chat con IA.
    
    Orquesta la interacción entre el repositorio de productos,
    el repositorio de chat y el servicio de IA de Gemini para
    proporcionar respuestas contextuales a los usuarios.
    
    Attributes:
        product_repo (IProductRepository): Repositorio de productos.
        chat_repo (IChatRepository): Repositorio de mensajes de chat.
        ai_service: Servicio de IA de Google Gemini.
    """

    def __init__(self, product_repo: IProductRepository, chat_repo: IChatRepository, ai_service):
        """
        Inicializa el servicio con los repositorios y servicio de IA.
        
        Args:
            product_repo (IProductRepository): Repositorio de productos.
            chat_repo (IChatRepository): Repositorio de chat.
            ai_service: Servicio de inteligencia artificial.
        """
        self.product_repo = product_repo
        self.chat_repo = chat_repo
        self.ai_service = ai_service

    async def process_message(self, request: ChatMessageRequestDTO) -> ChatMessageResponseDTO:
        """
        Procesa un mensaje del usuario y genera una respuesta con IA.
        
        Realiza el flujo completo:
        1. Obtiene productos disponibles.
        2. Recupera historial de conversación.
        3. Genera respuesta con IA usando contexto.
        4. Guarda mensaje del usuario y respuesta.
        5. Retorna la respuesta.
        
        Args:
            request (ChatMessageRequestDTO): Mensaje del usuario con session_id.
        
        Returns:
            ChatMessageResponseDTO: Respuesta generada por la IA con timestamp.
        
        Raises:
            ChatServiceError: Si hay un error al procesar el mensaje.
        """
        try:
            products = self.product_repo.get_all()
            history = self.chat_repo.get_recent_messages(request.session_id, count=6)
            context = ChatContext(messages=history)

            assistant_message = await self.ai_service.generate_response(
                user_message=request.message,
                products=products,
                context=context
            )

            now = datetime.utcnow()

            user_msg = ChatMessage(
                id=None,
                session_id=request.session_id,
                role='user',
                message=request.message,
                timestamp=now
            )
            self.chat_repo.save_message(user_msg)

            assistant_msg = ChatMessage(
                id=None,
                session_id=request.session_id,
                role='assistant',
                message=assistant_message,
                timestamp=now
            )
            self.chat_repo.save_message(assistant_msg)

            return ChatMessageResponseDTO(
                session_id=request.session_id,
                user_message=request.message,
                assistant_message=assistant_message,
                timestamp=now
            )

        except Exception as e:
            traceback.print_exc()
            raise ChatServiceError(f"Error al procesar el mensaje: {str(e)}")

    def get_session_history(self, session_id: str, limit: Optional[int] = 10) -> List[ChatHistoryDTO]:
        """
        Obtiene el historial de mensajes de una sesión.
        
        Args:
            session_id (str): Identificador de la sesión.
            limit (Optional[int]): Número máximo de mensajes a retornar.
        
        Returns:
            List[ChatHistoryDTO]: Lista de mensajes del historial.
        """
        messages = self.chat_repo.get_session_history(session_id, limit=limit)
        return [ChatHistoryDTO(
            id=msg.id,
            role=msg.role,
            message=msg.message,
            timestamp=msg.timestamp
        ) for msg in messages]

    def clear_session_history(self, session_id: str) -> int:
        """
        Elimina todo el historial de una sesión de chat.
        
        Args:
            session_id (str): Identificador de la sesión a limpiar.
        
        Returns:
            int: Cantidad de mensajes eliminados.
        """
        return self.chat_repo.delete_session_history(session_id)