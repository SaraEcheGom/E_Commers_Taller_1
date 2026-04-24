import pytest
from src.domain.entities import Product, ChatMessage, ChatContext
from datetime import datetime


def test_product_valid():
    p = Product(id=1, name="Nike", brand="Nike", category="Running",
                size="42", color="Negro", price=120.0, stock=5, description="test")
    assert p.is_available() == True


def test_product_invalid_price():
    with pytest.raises(ValueError):
        Product(id=1, name="Nike", brand="Nike", category="Running",
                size="42", color="Negro", price=-10.0, stock=5, description="test")


def test_product_invalid_stock():
    with pytest.raises(ValueError):
        Product(id=1, name="Nike", brand="Nike", category="Running",
                size="42", color="Negro", price=100.0, stock=-1, description="test")


def test_product_reduce_stock():
    p = Product(id=1, name="Nike", brand="Nike", category="Running",
                size="42", color="Negro", price=120.0, stock=5, description="test")
    p.reduce_stock(3)
    assert p.stock == 2


def test_product_reduce_stock_insufficient():
    p = Product(id=1, name="Nike", brand="Nike", category="Running",
                size="42", color="Negro", price=120.0, stock=2, description="test")
    with pytest.raises(ValueError):
        p.reduce_stock(5)


def test_chat_message_invalid_role():
    with pytest.raises(ValueError):
        ChatMessage(id=1, session_id="abc", role="admin",
                    message="hola", timestamp=datetime.utcnow())


def test_chat_message_empty_message():
    with pytest.raises(ValueError):
        ChatMessage(id=1, session_id="abc", role="user",
                    message="", timestamp=datetime.utcnow())


def test_chat_context_format():
    msgs = [
        ChatMessage(id=1, session_id="abc", role="user",
                    message="Hola", timestamp=datetime.utcnow()),
        ChatMessage(id=2, session_id="abc", role="assistant",
                    message="Hola! ¿En qué te ayudo?", timestamp=datetime.utcnow()),
    ]
    ctx = ChatContext(messages=msgs)
    result = ctx.format_for_prompt()
    assert "Usuario: Hola" in result
    assert "Asistente: Hola! ¿En qué te ayudo?" in result