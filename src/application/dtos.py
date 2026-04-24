"""
Módulo de DTOs (Data Transfer Objects).
Define los objetos para transferir datos entre capas con validación Pydantic.
"""

from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime


class ProductDTO(BaseModel):
    """
    DTO para transferir datos de productos entre capas.
    
    Incluye validaciones automáticas con Pydantic para garantizar
    que los datos sean correctos antes de procesarlos.
    
    Attributes:
        id (Optional[int]): Identificador único del producto.
        name (str): Nombre del producto.
        brand (str): Marca del producto.
        category (str): Categoría del producto.
        size (str): Talla del producto.
        color (str): Color del producto.
        price (float): Precio del producto, debe ser mayor a 0.
        stock (int): Stock disponible, no puede ser negativo.
        description (str): Descripción del producto.
    """
    id: Optional[int] = None
    name: str
    brand: str
    category: str
    size: str
    color: str
    price: float
    stock: int
    description: str

    @field_validator('price')
    @classmethod
    def price_must_be_positive(cls, v):
        """
        Valida que el precio sea mayor a 0.
        
        Args:
            v (float): Valor del precio a validar.
        
        Returns:
            float: El precio validado.
        
        Raises:
            ValueError: Si el precio es menor o igual a 0.
        """
        if v <= 0:
            raise ValueError("El precio debe ser mayor a 0")
        return v

    @field_validator('stock')
    @classmethod
    def stock_must_be_non_negative(cls, v):
        """
        Valida que el stock no sea negativo.
        
        Args:
            v (int): Valor del stock a validar.
        
        Returns:
            int: El stock validado.
        
        Raises:
            ValueError: Si el stock es negativo.
        """
        if v < 0:
            raise ValueError("El stock no puede ser negativo")
        return v

    class Config:
        from_attributes = True


class ChatMessageRequestDTO(BaseModel):
    """
    DTO para recibir mensajes del usuario en el chat.
    
    Attributes:
        session_id (str): Identificador único de la sesión del usuario.
        message (str): Contenido del mensaje enviado por el usuario.
    """
    session_id: str
    message: str

    @field_validator('message')
    @classmethod
    def message_not_empty(cls, v):
        """
        Valida que el mensaje no esté vacío.
        
        Args:
            v (str): Mensaje a validar.
        
        Returns:
            str: El mensaje validado.
        
        Raises:
            ValueError: Si el mensaje está vacío.
        """
        if not v.strip():
            raise ValueError("El mensaje no puede estar vacío")
        return v

    @field_validator('session_id')
    @classmethod
    def session_id_not_empty(cls, v):
        """
        Valida que el session_id no esté vacío.
        
        Args:
            v (str): Session ID a validar.
        
        Returns:
            str: El session_id validado.
        
        Raises:
            ValueError: Si el session_id está vacío.
        """
        if not v.strip():
            raise ValueError("El session_id no puede estar vacío")
        return v


class ChatMessageResponseDTO(BaseModel):
    """
    DTO para enviar la respuesta del chat al cliente.
    
    Attributes:
        session_id (str): Identificador de la sesión.
        user_message (str): Mensaje original del usuario.
        assistant_message (str): Respuesta generada por la IA.
        timestamp (datetime): Fecha y hora de la respuesta.
    """
    session_id: str
    user_message: str
    assistant_message: str
    timestamp: datetime


class ChatHistoryDTO(BaseModel):
    """
    DTO para mostrar el historial de mensajes de una sesión.
    
    Attributes:
        id (int): Identificador único del mensaje.
        role (str): Rol del emisor ('user' o 'assistant').
        message (str): Contenido del mensaje.
        timestamp (datetime): Fecha y hora del mensaje.
    """
    id: int
    role: str
    message: str
    timestamp: datetime

    class Config:
        from_attributes = True