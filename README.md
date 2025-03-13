# Ayuntamiento Chatbot API

## Descripción

API desarrollada con **FastAPI** que responde a mensajes de texto de usuarios de una página web de un ayuntamiento. La API almacena las conversaciones en una base de datos y genera respuestas utilizando **LangGraph**.

## Tecnologías

- **FastAPI**: Para la creación de la API REST.
- **SQLAlchemy**: Para la interacción con la base de datos que almacena las conversaciones.
- **Alembic**: Para gestionar migraciones de la base de datos.
- **PostgreSQL**: Base de datos relacional utilizada.
- **LangGraph**: Para generar respuestas automáticas basadas en datos almacenados.
- **ChromaDB**: Para el almacenamiento y búsqueda de embeddings.
- **Poetry**: Para la gestión de dependencias.
- **Docker & Docker Compose**: Para la contenedorización de la aplicación.
- **BeautifulSoup4**: Para realizar web scraping de la web.

---

## Instalación y Configuración

### 1. Clonar el repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd ayuntamiento-chatbot
```

### 2. Configurar entorno virtual y dependencias

Con **Poetry** instalado, ejecuta:

```bash
poetry install
```

### 3. Configurar variables de entorno

El archivo **.env** contiene la configuración de la base de datos:

```env
DATABASE_URL=postgresql://postgres:postgres@db:5432/ayuntamientochatbot
```

### 4. Aplicar migraciones de base de datos

Ejecutar las migraciones para crear la estructura de la base de datos:

```bash
poetry run alembic upgrade head
```

### 5. Ejecutar la aplicación localmente

Inicia el servidor de FastAPI con:

```bash
poetry run uvicorn main:app --reload
```

La API estará disponible en: [**http://127.0.0.1:8000**](http://127.0.0.1:8000)

---

## Uso con Docker

### 1. Construir y levantar los contenedores

```bash
docker-compose up --build
```

La API estará disponible en: [**http://localhost:8000**](http://localhost:8000)

### 2. Detener los contenedores

```bash
docker-compose down
```

---

## Endpoints de la API

### 1. Generar respuesta del chatbot

**POST** `/chat/`

- **Request** (JSON):

```json
{
    "message": "¿Cuáles son los eventos de esta semana?"
}
```

- **Response** (JSON):

```json
{
    "response": "El evento más cercano es el Taller de Circo el 15 de marzo."
}
```

### 2. Actualizar base de datos con nueva información

**GET** `/actualizar/?url=<URL_DEL_AYUNTAMIENTO>`

Descarga y almacena contenido web relevante en la base de datos vectorial.

---

## Estructura del Proyecto

```
├── app/
│   ├── main.py          # Punto de entrada de la API
│   ├── crud.py          # Para interactuar con la base de datos y guardar las conversaciones
│   ├── database.py      # Configuración de la base de datos
│   ├── dependencies.py  # Dependencias comunes
│   ├── langgraph_utils.py  # Generación de respuestas con LanChain y LangGraph
│   ├── models.py        # Definición de modelos SQLAlchemy
│   ├── schemas.py       # Esquemas de validación con Pydantic
│   ├── vector_store.py  # Gestión del almacén vectorial con embeddings
│   ├── web_scraper.py   # Scraping de contenido web
│   ├── .env             # Variables de entorno
├── migrations/          # Migraciones de Alembic
├── docker-compose.yml   # Configuración para Docker
├── Dockerfile           # Dockerfile para contenedorización
├── pyproject.toml       # Dependencias gestionadas con Poetry
└── README.md            # Documentación del proyecto
```

---

## Notas Técnicas

- **Almacenamiento de conversaciones**: Los mensajes del usuario y las respuestas del chatbot se guardan en la tabla `chat_messages` de PostgreSQL.
- **Generación de respuestas**: Se usa **LangGraph** para estructurar el flujo de procesamiento de respuestas con un modelo de IA.
- **Web Scraping**: Se extrae información de sitios web de ayuntamientos usando **BeautifulSoup4** y se almacena en ChromaDB para futuras consultas.

---
