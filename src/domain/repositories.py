"""
Módulo de interfaces de repositorios del dominio.
Define los contratos para el acceso a datos sin implementación concreta.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from .entities import Product, ChatMessage


class IProductRepository(ABC):
    """
    Interface que define el contrato para acceder a productos.
    
    Las implementaciones concretas estarán en la capa de infraestructura
    y pueden usar cualquier tecnología de persistencia.
    """

    @abstractmethod
    def get_all(self) -> List[Product]:
        """
        Obtiene todos los productos del sistema.
        
        Returns:
            List[Product]: Lista de todos los productos.
        """
        pass

    @abstractmethod
    def get_by_id(self, product_id: int) -> Optional[Product]:
        """
        Obtiene un producto por su identificador único.
        
        Args:
            product_id (int): ID del producto a buscar.
        
        Returns:
            Optional[Product]: El producto encontrado o None si no existe.
        """
        pass

    @abstractmethod
    def get_by_brand(self, brand: str) -> List[Product]:
        """
        Obtiene todos los productos de una marca específica.
        
        Args:
            brand (str): Nombre de la marca a filtrar.
        
        Returns:
            List[Product]: Lista de productos de la marca.
        """
        pass

    @abstractmethod
    def get_by_category(self, category: str) -> List[Product]:
        """
        Obtiene todos los productos de una categoría específica.
        
        Args:
            category (str): Nombre de la categoría a filtrar.
        
        Returns:
            List[Product]: Lista de productos de la categoría.
        """
        pass

    @abstractmethod
    def save(self, product: Product) -> Product:
        """
        Guarda o actualiza un producto en el sistema.
        
        Args:
            product (Product): Producto a guardar.
        
        Returns:
            Product: El producto guardado con su ID asignado.
        """
        pass

    @abstractmethod
    def delete(self, product_id: int) -> bool:
        """
        Elimina un producto por su identificador único.
        
        Args:
            product_id (int): ID del producto a eliminar.
        
        Returns:
            bool: True si se eliminó, False si no existía.
        """
        pass


class IChatRepository(ABC):
    """
    Interface que define el contrato para gestionar el historial de chat.
    
    Permite guardar y recuperar mensajes para mantener
    el contexto conversacional entre el usuario y la IA.
    """

    @abstractmethod
    def save_message(self, message: ChatMessage) -> ChatMessage:
        """
        Guarda un mensaje en el historial de conversación.
        
        Args:
            message (ChatMessage): Mensaje a guardar.
        
        Returns:
            ChatMessage: El mensaje guardado con su ID asignado.
        """
        pass

    @abstractmethod
    def get_session_history(self, session_id: str, limit: Optional[int] = None) -> List[ChatMessage]:
        """
        Obtiene el historial completo de una sesión de chat.
        
        Args:
            session_id (str): Identificador de la sesión.
            limit (Optional[int]): Número máximo de mensajes a retornar.
        
        Returns:
            List[ChatMessage]: Lista de mensajes en orden cronológico.
        """
        pass

    @abstractmethod
    def delete_session_history(self, session_id: str) -> int:
        """
        Elimina todo el historial de una sesión de chat.
        
        Args:
            session_id (str): Identificador de la sesión a eliminar.
        
        Returns:
            int: Cantidad de mensajes eliminados.
        """
        pass

    @abstractmethod
    def get_recent_messages(self, session_id: str, count: int) -> List[ChatMessage]:
        """
        Obtiene los últimos N mensajes de una sesión.
        
        Args:
            session_id (str): Identificador de la sesión.
            count (int): Número de mensajes a retornar.
        
        Returns:
            List[ChatMessage]: Lista de mensajes en orden cronológico.
        """
        pass