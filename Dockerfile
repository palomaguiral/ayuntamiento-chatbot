# Usa Python 3.9 como base
FROM python:3.9

# Define el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos de dependencias antes de instalar
COPY pyproject.toml poetry.lock ./

# Instala Poetry sin usar cache (+evita que Poetry cree entornos virtuales dentro de Docker, ya que el contenedor en sí ya es un entorno aislado) (+ evitar problemas de timeout)
RUN pip install --no-cache-dir poetry \
    && poetry config virtualenvs.create false \
    && poetry config installer.max-workers 1

# Evita la instalación de paquetes CUDA en torch
RUN poetry run pip install --no-cache-dir --extra-index-url https://download.pytorch.org/whl/cpu torch torchvision torchaudio

# Instala las dependencias del proyecto
RUN poetry install --no-root --no-cache --no-interaction

# Copia el resto de los archivos del proyecto
COPY . .

# Expone el puerto 8000
EXPOSE 8000

# Comando para ejecutar la API
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
