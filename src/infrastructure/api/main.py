"""
Módulo principal de la API.
Define la aplicación FastAPI con todos los endpoints del e-commerce.
"""

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from src.infrastructure.db.database import get_db, init_db
from src.infrastructure.repositories.product_repository import SQLProductRepository
from src.infrastructure.repositories.chat_repository import SQLChatRepository
from src.infrastructure.llm_providers.gemini_service import GeminiService
from src.application.product_service import ProductService
from src.application.chat_service import ChatService
from src.application.dtos import (
    ProductDTO, ChatMessageRequestDTO,
    ChatMessageResponseDTO, ChatHistoryDTO
)
from src.domain.exceptions import ProductNotFoundError

app = FastAPI(
    title="E-commerce Chat IA",
    description="API de e-commerce de zapatos con chat inteligente",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="."), name="static")


@app.on_event("startup")
def startup():
    """Inicializa la base de datos al arrancar la aplicación."""
    init_db()


@app.get("/frontend", include_in_schema=False)
def frontend():
    """Sirve el frontend de Stephora."""
    return FileResponse("index.html")


@app.get("/")
def root():
    """
    Endpoint raíz que retorna información básica de la API.

    Returns:
        dict: Nombre, versión y endpoints disponibles.
    """
    return {
        "name": "E-commerce Chat IA",
        "version": "1.0.0",
        "endpoints": ["/products", "/chat", "/health", "/docs", "/frontend"]
    }


@app.get("/health")
def health():
    """
    Health check para verificar que la API está funcionando.

    Returns:
        dict: Estado de la API y timestamp actual.
    """
    return {"status": "ok", "timestamp": datetime.utcnow()}


@app.get("/products")
def get_products(db: Session = Depends(get_db)):
    """
    Obtiene la lista completa de productos disponibles.

    Args:
        db (Session): Sesión de base de datos inyectada por FastAPI.

    Returns:
        List[Product]: Lista de todos los productos.
    """
    try:
        repo = SQLProductRepository(db)
        service = ProductService(repo)
        result = service.get_all_products()
        return result
    except Exception as e:
        import traceback
        print("ERROR EN PRODUCTS:", e)
        traceback.print_exc()
        return {"error": str(e)}


@app.get("/products/{product_id}", response_model=ProductDTO)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """
    Obtiene un producto específico por su ID.

    Args:
        product_id (int): ID del producto a buscar.
        db (Session): Sesión de base de datos inyectada por FastAPI.

    Returns:
        ProductDTO: Datos del producto encontrado.

    Raises:
        HTTPException: 404 si el producto no existe.
    """
    repo = SQLProductRepository(db)
    service = ProductService(repo)
    try:
        return service.get_product_by_id(product_id)
    except ProductNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.post("/chat", response_model=ChatMessageResponseDTO)
async def chat(request: ChatMessageRequestDTO, db: Session = Depends(get_db)):
    """
    Procesa un mensaje del usuario y retorna la respuesta de la IA.

    Args:
        request (ChatMessageRequestDTO): Mensaje del usuario con session_id.
        db (Session): Sesión de base de datos inyectada por FastAPI.

    Returns:
        ChatMessageResponseDTO: Respuesta generada por la IA.

    Raises:
        HTTPException: 500 si hay un error al procesar el mensaje.
    """
    product_repo = SQLProductRepository(db)
    chat_repo = SQLChatRepository(db)
    ai_service = GeminiService()
    service = ChatService(product_repo, chat_repo, ai_service)
    try:
        return await service.process_message(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/chat/history/{session_id}", response_model=List[ChatHistoryDTO])
def get_history(session_id: str, limit: int = 10, db: Session = Depends(get_db)):
    """
    Obtiene el historial de mensajes de una sesión de chat.

    Args:
        session_id (str): Identificador de la sesión.
        limit (int): Número máximo de mensajes a retornar.
        db (Session): Sesión de base de datos inyectada por FastAPI.

    Returns:
        List[ChatHistoryDTO]: Lista de mensajes del historial.
    """
    product_repo = SQLProductRepository(db)
    chat_repo = SQLChatRepository(db)
    ai_service = GeminiService()
    service = ChatService(product_repo, chat_repo, ai_service)
    return service.get_session_history(session_id, limit)


@app.delete("/chat/history/{session_id}")
def delete_history(session_id: str, db: Session = Depends(get_db)):
    """
    Elimina el historial de mensajes de una sesión de chat.

    Args:
        session_id (str): Identificador de la sesión a limpiar.
        db (Session): Sesión de base de datos inyectada por FastAPI.

    Returns:
        dict: Cantidad de mensajes eliminados y session_id.
    """
    product_repo = SQLProductRepository(db)
    chat_repo = SQLChatRepository(db)
    ai_service = GeminiService()
    service = ChatService(product_repo, chat_repo, ai_service)
    deleted = service.clear_session_history(session_id)
    return {"deleted": deleted, "session_id": session_id}