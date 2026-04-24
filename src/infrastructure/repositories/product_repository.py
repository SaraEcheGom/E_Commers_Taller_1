"""
Módulo del repositorio de productos.
Implementa el acceso a datos de productos usando SQLAlchemy.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from src.domain.entities import Product
from src.domain.repositories import IProductRepository
from src.infrastructure.db.models import ProductModel


class SQLProductRepository(IProductRepository):
    """
    Implementación del repositorio de productos usando SQLAlchemy.
    
    Gestiona el acceso a la tabla de productos en la base de datos
    SQLite, convirtiendo entre modelos ORM y entidades del dominio.
    
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

    def get_all(self) -> List[Product]:
        """
        Obtiene todos los productos de la base de datos.
        
        Returns:
            List[Product]: Lista de todos los productos como entidades.
        """
        models = self.db.query(ProductModel).all()
        return [self._model_to_entity(m) for m in models]

    def get_by_id(self, product_id: int) -> Optional[Product]:
        """
        Obtiene un producto por su ID.
        
        Args:
            product_id (int): ID del producto a buscar.
        
        Returns:
            Optional[Product]: El producto encontrado o None.
        """
        model = self.db.query(ProductModel).filter(ProductModel.id == product_id).first()
        return self._model_to_entity(model) if model else None

    def get_by_brand(self, brand: str) -> List[Product]:
        """
        Obtiene productos filtrados por marca.
        
        Args:
            brand (str): Nombre de la marca a filtrar.
        
        Returns:
            List[Product]: Lista de productos de la marca.
        """
        models = self.db.query(ProductModel).filter(ProductModel.brand == brand).all()
        return [self._model_to_entity(m) for m in models]

    def get_by_category(self, category: str) -> List[Product]:
        """
        Obtiene productos filtrados por categoría.
        
        Args:
            category (str): Nombre de la categoría a filtrar.
        
        Returns:
            List[Product]: Lista de productos de la categoría.
        """
        models = self.db.query(ProductModel).filter(ProductModel.category == category).all()
        return [self._model_to_entity(m) for m in models]

    def save(self, product: Product) -> Product:
        """
        Guarda o actualiza un producto en la base de datos.
        
        Args:
            product (Product): Producto a guardar.
        
        Returns:
            Product: El producto guardado con su ID asignado.
        """
        if product.id:
            model = self.db.query(ProductModel).filter(ProductModel.id == product.id).first()
            model.name = product.name
            model.brand = product.brand
            model.category = product.category
            model.size = product.size
            model.color = product.color
            model.price = product.price
            model.stock = product.stock
            model.description = product.description
        else:
            model = self._entity_to_model(product)
            self.db.add(model)

        self.db.commit()
        self.db.refresh(model)
        return self._model_to_entity(model)

    def delete(self, product_id: int) -> bool:
        """
        Elimina un producto de la base de datos.
        
        Args:
            product_id (int): ID del producto a eliminar.
        
        Returns:
            bool: True si se eliminó, False si no existía.
        """
        model = self.db.query(ProductModel).filter(ProductModel.id == product_id).first()
        if not model:
            return False
        self.db.delete(model)
        self.db.commit()
        return True

    def _model_to_entity(self, model: ProductModel) -> Product:
        """
        Convierte un modelo ORM a una entidad del dominio.
        
        Args:
            model (ProductModel): Modelo ORM a convertir.
        
        Returns:
            Product: Entidad del dominio correspondiente.
        """
        return Product(
            id=model.id,
            name=model.name,
            brand=model.brand,
            category=model.category,
            size=model.size,
            color=model.color,
            price=model.price,
            stock=model.stock,
            description=model.description
        )

    def _entity_to_model(self, product: Product) -> ProductModel:
        """
        Convierte una entidad del dominio a un modelo ORM.
        
        Args:
            product (Product): Entidad a convertir.
        
        Returns:
            ProductModel: Modelo ORM correspondiente.
        """
        return ProductModel(
            name=product.name,
            brand=product.brand,
            category=product.category,
            size=product.size,
            color=product.color,
            price=product.price,
            stock=product.stock,
            description=product.description
        )