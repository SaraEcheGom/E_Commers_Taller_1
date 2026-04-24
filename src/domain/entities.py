"""
Módulo de entidades del dominio.
Define las entidades principales del e-commerce con su lógica de negocio.
"""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Product:
    """
    Entidad que representa un producto (zapato) en el e-commerce.
    
    Contiene la lógica de negocio relacionada con productos,
    incluyendo validaciones de precio, stock y disponibilidad.
    
    Attributes:
        id (Optional[int]): Identificador único del producto.
        name (str): Nombre del producto.
        brand (str): Marca del producto.
        category (str): Categoría del producto (Running, Casual, Formal).
        size (str): Talla del producto.
        color (str): Color del producto.
        price (float): Precio en dólares, debe ser mayor a 0.
        stock (int): Cantidad disponible en inventario.
        description (str): Descripción del producto.
    """
    id: Optional[int]
    name: str
    brand: str
    category: str
    size: str
    color: str
    price: float
    stock: int
    description: str

    def __post_init__(self):
        """
        Valida los datos del producto después de la inicialización.
        
        Raises:
            ValueError: Si el nombre está vacío, el precio es menor o igual
                       a 0, o el stock es negativo.
        """
        if not self.name:
            raise ValueError("El nombre no puede estar vacío")
        if self.price <= 0:
            raise ValueError("El precio debe ser mayor a 0")
        if self.stock < 0:
            raise ValueError("El stock no puede ser negativo")

    def is_available(self) -> bool:
        """
        Verifica si el producto tiene stock disponible.
        
        Returns:
            bool: True si el stock es mayor a 0, False en caso contrario.
        """
        return self.stock > 0

    def reduce_stock(self, quantity: int) -> None:
        """
        Reduce el stock del producto en la cantidad especificada.
        
        Args:
            quantity (int): Cantidad a reducir. Debe ser positiva.
        
        Raises:
            ValueError: Si la cantidad es negativa o mayor al stock disponible.
        """
        if quantity <= 0:
            raise ValueError("La cantidad debe ser positiva")
        if quantity > self.stock:
            raise ValueError("Stock insuficiente")
        self.stock -= quantity

    def increase_stock(self, quantity: int) -> None:
        """
        Aumenta el stock del producto en la cantidad especificada.
        
        Args:
            quantity (int): Cantidad a aumentar. Debe ser positiva.
        
        Raises:
            ValueError: Si la cantidad es negativa.
        """
        if quantity <= 0:
            raise ValueError("La cantidad debe ser positiva")
        self.stock += quantity


@dataclass
class ChatMessage:
    """
    Entidad que representa un mensaje en el chat conversacional.
    
    Attributes:
        id (Optional[int]): Identificador único del mensaje.
        session_id (str): Identificador de la sesión del usuario.
        role (str): Rol del emisor, puede ser 'user' o 'assistant'.
        message (str): Contenido del mensaje.
        timestamp (datetime): Fecha y hora del mensaje.
    """
    id: Optional[int]
    session_id: str
    role: str
    message: str
    timestamp: datetime

    def __post_init__(self):
        """
        Valida los datos del mensaje después de la inicialización.
        
        Raises:
            ValueError: Si el role no es válido, el mensaje está vacío
                       o el session_id está vacío.
        """
        if self.role not in ('user', 'assistant'):
            raise ValueError("El role debe ser 'user' o 'assistant'")
        if not self.message:
            raise ValueError("El mensaje no puede estar vacío")
        if not self.session_id:
            raise ValueError("El session_id no puede estar vacío")

    def is_from_user(self) -> bool:
        """
        Verifica si el mensaje fue enviado por el usuario.
        
        Returns:
            bool: True si el role es 'user'.
        """
        return self.role == 'user'

    def is_from_assistant(self) -> bool:
        """
        Verifica si el mensaje fue enviado por el asistente.
        
        Returns:
            bool: True si el role es 'assistant'.
        """
        return self.role == 'assistant'


@dataclass
class ChatContext:
    """
    Value Object que encapsula el contexto de una conversación.
    
    Mantiene los mensajes recientes para dar coherencia al chat
    y permitir que la IA tenga memoria de la conversación.
    
    Attributes:
        messages (list): Lista de mensajes de la conversación.
        max_messages (int): Número máximo de mensajes a considerar.
    """
    messages: list
    max_messages: int = 6

    def get_recent_messages(self) -> list:
        """
        Retorna los últimos N mensajes de la conversación.
        
        Returns:
            list: Lista con los últimos max_messages mensajes.
        """
        return self.messages[-self.max_messages:]

    def format_for_prompt(self) -> str:
        """
        Formatea los mensajes recientes para incluirlos en el prompt de IA.
        
        Returns:
            str: Historial formateado con el rol y mensaje de cada participante.
        
        Example:
            >>> ctx.format_for_prompt()
            'Usuario: Hola\\nAsistente: ¡Hola! ¿En qué te ayudo?'
        """
        lines = []
        for msg in self.get_recent_messages():
            role = "Usuario" if msg.is_from_user() else "Asistente"
            lines.append(f"{role}: {msg.message}")
        return "\n".join(lines)