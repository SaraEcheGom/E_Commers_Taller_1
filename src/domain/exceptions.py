"""
Módulo de excepciones del dominio.
Define errores específicos del negocio para el e-commerce.
"""


class ProductNotFoundError(Exception):
    """
    Excepción que se lanza cuando un producto no existe en el sistema.
    
    Attributes:
        message (str): Mensaje descriptivo del error.
    """
    
    def __init__(self, product_id: int = None):
        """
        Inicializa la excepción con un mensaje descriptivo.
        
        Args:
            product_id (int, optional): ID del producto no encontrado.
        """
        if product_id:
            self.message = f"Producto con ID {product_id} no encontrado"
        else:
            self.message = "Producto no encontrado"
        super().__init__(self.message)


class InvalidProductDataError(Exception):
    """
    Excepción que se lanza cuando los datos de un producto son inválidos.
    
    Attributes:
        message (str): Mensaje descriptivo del error.
    """
    
    def __init__(self, message: str = "Datos de producto inválidos"):
        """
        Inicializa la excepción con un mensaje personalizado.
        
        Args:
            message (str): Mensaje descriptivo del error.
        """
        self.message = message
        super().__init__(self.message)


class ChatServiceError(Exception):
    """
    Excepción que se lanza cuando hay un error en el servicio de chat.
    
    Attributes:
        message (str): Mensaje descriptivo del error.
    """
    
    def __init__(self, message: str = "Error en el servicio de chat"):
        """
        Inicializa la excepción con un mensaje personalizado.
        
        Args:
            message (str): Mensaje descriptivo del error.
        """
        self.message = message
        super().__init__(self.message)