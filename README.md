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
git clone https://github.com/SaraEcheGom/E_Commers_Taller_1.git
cd E_Commers_Taller_1
```

2. Crear entorno virtual

```bash
python -m venv venv
venv\Scripts\activate
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
| Frontend | http://localhost:8001/frontend |

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
| GET | `/frontend` | Frontend de Stephora |

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

```
e-commerce-chat-ai/
├── src/
│   ├── domain/          # Entidades y reglas de negocio
│   ├── application/     # Servicios y casos de uso
│   └── infrastructure/  # API, base de datos y servicios externos
├── tests/               # Tests unitarios
├── data/                # Base de datos SQLite
├── index.html           # Frontend Stephora
├── logo.jpeg            # Logo
├── Dockerfile
├── docker-compose.yml
└── README.md
```
## Evidencias

<table>
  <tr>
    <td><img width="400" alt="Swagger UI" src="https://github.com/user-attachments/assets/792537ee-e0b0-476c-bc23-1594bf526723" /></td>
    <td><img width="400" alt="Frontend Home" src="https://github.com/user-attachments/assets/dfc9804e-0522-44e3-af78-39ae1748793b" /></td>
  </tr>
  <tr>
    <td><img width="400" alt="Frontend Productos" src="https://github.com/user-attachments/assets/8005008f-42e2-4f94-b92c-14e78a69e88b" /></td>
    <td><img width="400" alt="Frontend Chat" src="https://github.com/user-attachments/assets/8160513c-1386-4911-8ef4-110376d5230f" /></td>
  </tr>
  <tr>
    <td><img width="400" alt="API Products" src="https://github.com/user-attachments/assets/e9c71a62-5e48-4c1e-af91-1f2ddf00682e" /></td>
    <td><img width="400" alt="Chat Response" src="https://github.com/user-attachments/assets/c788309f-cb91-4d78-b53d-9c725ff48694" /></td>
  </tr>
  <tr>
    <td><img width="400" alt="Base de Datos" src="https://github.com/user-attachments/assets/ee909f11-4bee-4e47-b7c3-4e6dfb508d54" /></td>
    <td><img width="400" alt="Docker Running" src="https://github.com/user-attachments/assets/40980c83-10c5-4693-b848-5eb4ed549789" /></td>
  </tr>
  <tr>
    <td><img width="400" alt="Docker Logs" src="https://github.com/user-attachments/assets/d8de7b5f-aeb1-4f06-9427-9bfa22e09412" /></td>
    <td><img width="400" alt="Tests Passing" src="https://github.com/user-attachments/assets/83fbe4fc-d11b-4341-a91c-5584a8c5361f" /></td>
  </tr>
  <tr>
    <td><img width="400" alt="Chat IA" src="https://github.com/user-attachments/assets/6df1e365-dc2d-4846-9591-8829ee93b52d" /></td>
    <td><img width="400" alt="Tests Output" src="https://github.com/user-attachments/assets/925fb4ad-39a7-4c24-b801-d0d578754c66" /></td>
  </tr>
  <tr>
    <td><img width="400" alt="Frontend Stephora Home" src="https://github.com/user-attachments/assets/9add33f0-5340-4cd5-9b23-f76fb949e5fe" /></td>
    <td><img width="400" alt="Frontend Stephora Chat" src="https://github.com/user-attachments/assets/d50b9e69-766a-4b53-b34b-fd40d478188b" /></td>
  </tr>

</table>


## Autor
Sara Echeverri Gómez

