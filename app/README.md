# Documentación `/app`

La carpeta `/app` contiene todos los scripts necesarios para el funcionamiento de la API del chatbot del ayuntamiento. Estos scripts se pueden dividir en tres categorías principales:

1. **Chatbot y procesamiento de datos**: Maneja la obtención, almacenamiento y recuperación de información, así como la generación de respuestas automáticas.
2. **Gestión de la base de datos**: Administra el almacenamiento de conversaciones en la base de datos.
3. **API principal**: Define los endpoints de la API y gestiona las solicitudes.

---

## 1️⃣ Chatbot y procesamiento de datos
Estos archivos manejan la recopilación de información, la indexación en el almacén vectorial y la generación de respuestas.

### `langgraph_utils.py`
- Implementa la lógica del chatbot utilizando **LangGraph**.
- Crea un flujo estructurado para limpiar el texto, buscar información relevante por similitud semántica y generar respuestas con modelos de IA.
- Usa el modelo **Mistral (Ollama)** para la generación de respuestas.

### `vector_store.py`
- Utiliza **ChromaDB** para almacenar y buscar información relevante en formato de embeddings. 
- La base de datos se guarda en la carpeta /db.
- Usa el modelo de embeddings de **Hugging Face** ("sentence-transformers/all-MiniLM-L6-v2") para procesar y representar el contenido. Este modelo acepta un número bajo de tokens, si quisiéramos podríamos cambiar de modelo.
- Permite almacenar nuevos documentos (`almacenar_documentos(documentos)`)y realizar búsquedas semánticas eficientes (`buscar_respuesta(pregunta: str)`).

### `web_scraper.py`
- Extrae información de páginas web del ayuntamiento mediante **web scraping**.
- Intenta obtener las URLs desde un `sitemap.xml`, extrae su contenido y hace una búsqueda recursiva de los enlaces que pueda haber en dicho contenido.
- Utiliza **BeautifulSoup4** para limpiar y estructurar el contenido obtenido.

### `schemas.py`
- Define los esquemas de datos utilizando **Pydantic**.
- Garantiza la validación de datos para la API.
- Contiene las clases `ChatRequest` y `ChatResponse` que estructuran los datos de entrada y salida de la API, donde ambos deben ser de tipo string.

---

## 2️⃣ Gestión de la base de datos
Estos archivos manejan la conexión a la base de datos, la definición de modelos y la interacción con la base de datos.

### `database.py`
- Configura la conexión con **PostgreSQL** utilizando **SQLAlchemy**.
- Usa **Alembic** para manejar migraciones de la base de datos.
- Define la sesión de base de datos para las interacciones de la API.

### `crud.py`
- Para interactuar con la base de datos.
- Implementa la función `save_chat(db, user_message, bot_response)`, que almacena los mensajes del usuario y las respuestas del chatbot en la base de datos.

### `models.py`
- Define los modelos de base de datos utilizando **Declarative Mapping** de SQLAlchemy.
- Contiene el modelo `ChatMessage`, que representa la tabla `chat_messages`.
- Incluye los campos `id`, `user_message`, `bot_response` y `timestamp`.

---

## 3️⃣ API Principal
El archivo principal que gestiona las solicitudes HTTP y la lógica de la API.

### `main.py`
- Define la API utilizando **FastAPI**.
- Endpoint `/chat/`: recibe mensajes y devuelve respuestas generadas por el chatbot. Además, registra las conversaciones en la base de datos utilizando **SQLAlchemy**.
- Endpoint `/actualizar/`: que permite extraer y almacenar nueva información de una página web (por ejemplo: https://www.valencia.es) en la base de datos vectorial.

---
