"""
Módulo del servicio de IA con Google Gemini.
Implementa la integración con la API de Google Gemini para el chat.
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv
from src.domain.entities import ChatContext
from typing import List

load_dotenv()


class GeminiService:
    """
    Servicio de inteligencia artificial usando Google Gemini.
    
    Gestiona la comunicación con la API de Google Gemini para
    generar respuestas contextuales sobre productos de zapatos.
    
    Attributes:
        model: Modelo de Gemini configurado para generar contenido.
    """

    def __init__(self):
        """
        Inicializa el servicio configurando la API key y el modelo de Gemini.
        """
        api_key = os.getenv("GEMINI_API_KEY")
        print(f"API KEY cargada: {api_key[:10]}...")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-2.5-flash")

    def _format_products_info(self, products) -> str:
        """
        Formatea la lista de productos para incluirla en el prompt.
        
        Args:
            products (List): Lista de productos a formatear.
        
        Returns:
            str: Texto con los productos formateados.
        """
        lines = []
        for p in products:
            disponible = "Disponible" if p.is_available() else "Agotado"
            lines.append(f"- {p.name} | {p.brand} | Talla {p.size} | Color {p.color} | ${p.price} | Stock: {p.stock} | {disponible}")
        return "\n".join(lines)

    async def generate_response(self, user_message: str, products: List, context: ChatContext) -> str:
        """
        Genera una respuesta usando la IA de Google Gemini.
        
        Construye un prompt con los productos disponibles y el historial
        de conversación para generar respuestas contextuales.
        
        Args:
            user_message (str): Mensaje actual del usuario.
            products (List): Lista de productos disponibles.
            context (ChatContext): Contexto con el historial de conversación.
        
        Returns:
            str: Respuesta generada por la IA.
        
        Raises:
            Exception: Si hay un error al comunicarse con la API de Gemini.
        """
        products_info = self._format_products_info(products)
        conversation_history = context.format_for_prompt()

        prompt = f"""Eres un asistente virtual experto en ventas de zapatos para un e-commerce.
Tu objetivo es ayudar a los clientes a encontrar los zapatos perfectos.

PRODUCTOS DISPONIBLES:
{products_info}

INSTRUCCIONES:
- Sé amigable y profesional
- Usa el contexto de la conversación anterior si existe
- Recomienda productos específicos cuando sea apropiado
- Menciona precios, tallas y disponibilidad
- Responde siempre en español
- Si no tienes información, sé honesto

HISTORIAL DE CONVERSACIÓN:
{conversation_history}

Usuario: {user_message}
Asistente:"""

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            raise Exception(f"Error al comunicarse con Gemini: {str(e)}")