"""
Módulo de datos iniciales.
Carga productos de ejemplo en la base de datos si está vacía.
"""

from src.infrastructure.db.models import ProductModel


def load_initial_data(db):
    """
    Carga 10 productos iniciales en la base de datos.
    
    Verifica si ya existen productos antes de insertar
    para evitar duplicados en cada inicio de la aplicación.
    
    Args:
        db: Sesión activa de SQLAlchemy.
    """
    if db.query(ProductModel).count() > 0:
        return

    products = [
        ProductModel(name="Air Zoom Pegasus 40", brand="Nike", category="Running",
                     size="42", color="Negro", price=120.0, stock=5,
                     description="Zapatilla de running con amortiguación reactiva"),
        ProductModel(name="Ultraboost 23", brand="Adidas", category="Running",
                     size="41", color="Blanco", price=150.0, stock=3,
                     description="Máxima energía de retorno con suela Boost"),
        ProductModel(name="Suede Classic", brand="Puma", category="Casual",
                     size="40", color="Azul", price=80.0, stock=10,
                     description="Clásico urbano con parte superior de gamuza"),
        ProductModel(name="Chuck Taylor All Star", brand="Converse", category="Casual",
                     size="43", color="Blanco", price=65.0, stock=8,
                     description="El icónico zapato de lona para el día a día"),
        ProductModel(name="Old Skool", brand="Vans", category="Casual",
                     size="41", color="Negro/Blanco", price=70.0, stock=6,
                     description="Skate clásico con banda lateral característica"),
        ProductModel(name="Gel-Kayano 30", brand="Asics", category="Running",
                     size="42", color="Azul/Amarillo", price=160.0, stock=4,
                     description="Estabilidad máxima para corredores de larga distancia"),
        ProductModel(name="Fresh Foam 1080v13", brand="New Balance", category="Running",
                     size="43", color="Gris", price=175.0, stock=2,
                     description="Amortiguación premium para rodajes largos"),
        ProductModel(name="Derby Lace Up", brand="Clarks", category="Formal",
                     size="42", color="Marrón", price=110.0, stock=7,
                     description="Zapato formal de cuero para ocasiones de negocio"),
        ProductModel(name="Oxford Brogue", brand="Clarks", category="Formal",
                     size="41", color="Negro", price=130.0, stock=3,
                     description="Elegante zapato oxford con detalles broguing"),
        ProductModel(name="Speedcat", brand="Puma", category="Casual",
                     size="40", color="Rojo", price=90.0, stock=9,
                     description="Inspirado en el automovilismo, estilo retro deportivo"),
    ]

    db.add_all(products)
    db.commit()