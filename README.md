# E-commerce con Chat IA 🛍️

API REST de e-commerce de zapatos con chat inteligente usando Clean Architecture y Google Gemini AI.

## Descripción

Sistema que permite a los usuarios consultar productos de zapatos mediante endpoints REST tradicionales y conversar con un asistente de IA que les ayuda a encontrar el zapato perfecto, manteniendo memoria conversacional.

## Tecnologías

- **Python 3.13**
- **FastAPI** — Framework web para crear endpoints HTTP
- **SQLAlchemy** — ORM para base de datos
- **SQLite** — Base de datos ligera
- **Google Gemini AI** — Inteligencia artificial conversacional
- **Pydantic** — Validación de datos
- **Docker** — Containerización
- **Pytest** — Testing unitario

## Arquitectura

El proyecto implementa Clean Architecture con 3 capas:

- **Domain Layer** — Entidades y reglas de negocio puras
- **Application Layer** — Casos de uso y servicios
- **Infrastructure Layer** — Base de datos, API y servicios externos

## Instalación

### Requisitos Previos

- Python 3.10+
- Docker y Docker Compose
- API Key de Google Gemini

### Pasos

1. Clonar repositorio
```bash
git clone <tu-repo>
cd e-commerce-chat-ai
```

2. Crear entorno virtual
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
```

3. Instalar dependencias
```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno
```bash
cp .env.example .env
# Editar .env y agregar tu GEMINI_API_KEY
```

5. Ejecutar localmente
```bash
uvicorn src.infrastructure.api.main:app --reload --port 8001
```

6. Ejecutar con Docker
```bash
docker-compose up --build
```

## Uso

| Entorno | URL |
|---------|-----|
| Local | http://localhost:8001 |
| Docker | http://localhost:8080 |
| Documentación | http://localhost:8001/docs |

## Endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/` | Información de la API |
| GET | `/health` | Health check |
| GET | `/products` | Lista todos los productos |
| GET | `/products/{id}` | Obtiene un producto por ID |
| POST | `/chat` | Envía mensaje al chat con IA |
| GET | `/chat/history/{session_id}` | Obtiene historial de sesión |
| DELETE | `/chat/history/{session_id}` | Elimina historial de sesión |

## Ejemplo de Chat

**Request:**
```json
POST /chat
{
  "session_id": "usuario123",
  "message": "Hola, busco zapatos para correr"
}
```

**Response:**
```json
{
  "session_id": "usuario123",
  "user_message": "Hola, busco zapatos para correr",
  "assistant_message": "¡Hola! Tengo varias opciones para running...",
  "timestamp": "2026-04-24T21:04:56"
}
```

## Tests

```bash
pytest tests/ -v
```

## Estructura del Proyecto

e-commerce-chat-ai/
├── src/
│   ├── domain/          # Entidades y reglas de negocio
│   ├── application/     # Servicios y casos de uso
│   └── infrastructure/  # API, base de datos y servicios externos
├── tests/               # Tests unitarios
├── data/                # Base de datos SQLite
├── Dockerfile
├── docker-compose.yml
├── index.html           # Frontend
├── logo.jpeg            # Logo
└── README.md

## Autor
Sara Echeverri Gómez