# Imagen base de Python
FROM python:3.9

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar los archivos de Poetry primero para aprovechar la caché de Docker
COPY pyproject.toml poetry.lock ./

# Instalar Poetry y las dependencias
RUN pip install --no-cache-dir poetry && poetry install --no-root

# Instala psycopg2-binary para conectar con PostgreSQL
RUN poetry run pip install psycopg2-binary

# Copiar todo el código fuente del proyecto al contenedor
COPY . .

# Exponer el puerto en el que correrá la API
EXPOSE 8000

# Comando para ejecutar la API cuando el contenedor se inicie
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
