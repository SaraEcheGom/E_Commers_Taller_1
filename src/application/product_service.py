"""
Módulo del servicio de productos.
Implementa los casos de uso relacionados con la gestión de productos.
"""

from typing import List
from src.domain.entities import Product
from src.domain.repositories import IProductRepository
from src.domain.exceptions import ProductNotFoundError
from src.application.dtos import ProductDTO


class ProductService:
    """
    Servicio de aplicación para gestionar productos del e-commerce.
    
    Orquesta los casos de uso relacionados con productos, coordinando
    el acceso a datos a través del repositorio inyectado.
    
    Attributes:
        product_repo (IProductRepository): Repositorio de productos.
    """

    def __init__(self, product_repo: IProductRepository):
        """
        Inicializa el servicio con el repositorio de productos.
        
        Args:
            product_repo (IProductRepository): Repositorio de productos a usar.
        """
        self.product_repo = product_repo

    def get_all_products(self) -> List[Product]:
        """
        Obtiene todos los productos del sistema.
        
        Returns:
            List[Product]: Lista completa de productos.
        """
        return self.product_repo.get_all()

    def get_product_by_id(self, product_id: int) -> Product:
        """
        Obtiene un producto por su ID.
        
        Args:
            product_id (int): ID del producto a buscar.
        
        Returns:
            Product: El producto encontrado.
        
        Raises:
            ProductNotFoundError: Si el producto no existe.
        """
        product = self.product_repo.get_by_id(product_id)
        if not product:
            raise ProductNotFoundError(product_id)
        return product

    def get_available_products(self) -> List[Product]:
        """
        Obtiene solo los productos con stock disponible.
        
        Returns:
            List[Product]: Lista de productos disponibles.
        """
        products = self.product_repo.get_all()
        return [p for p in products if p.is_available()]

    def create_product(self, dto: ProductDTO) -> Product:
        """
        Crea un nuevo producto en el sistema.
        
        Args:
            dto (ProductDTO): Datos del producto a crear.
        
        Returns:
            Product: El producto creado con su ID asignado.
        """
        product = Product(
            id=None,
            name=dto.name,
            brand=dto.brand,
            category=dto.category,
            size=dto.size,
            color=dto.color,
            price=dto.price,
            stock=dto.stock,
            description=dto.description
        )
        return self.product_repo.save(product)

    def update_product(self, product_id: int, dto: ProductDTO) -> Product:
        """
        Actualiza un producto existente.
        
        Args:
            product_id (int): ID del producto a actualizar.
            dto (ProductDTO): Nuevos datos del producto.
        
        Returns:
            Product: El producto actualizado.
        
        Raises:
            ProductNotFoundError: Si el producto no existe.
        """
        existing = self.get_product_by_id(product_id)
        existing.name = dto.name
        existing.brand = dto.brand
        existing.category = dto.category
        existing.size = dto.size
        existing.color = dto.color
        existing.price = dto.price
        existing.stock = dto.stock
        existing.description = dto.description
        return self.product_repo.save(existing)

    def delete_product(self, product_id: int) -> bool:
        """
        Elimina un producto del sistema.
        
        Args:
            product_id (int): ID del producto a eliminar.
        
        Returns:
            bool: True si se eliminó correctamente.
        
        Raises:
            ProductNotFoundError: Si el producto no existe.
        """
        self.get_product_by_id(product_id)
        return self.product_repo.delete(product_id)