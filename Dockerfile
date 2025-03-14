# Usa Python 3.9 como base
FROM python:3.9

# Define el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos de dependencias antes de instalar
COPY pyproject.toml poetry.lock ./

# Instala Poetry sin usar cache
RUN pip install --no-cache-dir poetry \
    && poetry config virtualenvs.create false \
    && poetry config installer.max-workers 1

# Bloqueamos CUDA antes de instalar `torch`. Esto le dice a pip y torch que nunca instalen versiones con soporte CUDA.
# Los paquetes nvidia-cuda-runtime-cu12, nvidia-cudnn-cu12, nvidia-cublas-cu12, etc., requieren drivers CUDA y hardware NVIDIA para funcionar. Pero dentro de Docker (sin una configuración especial como nvidia-docker), no hay acceso a una GPU NVIDIA.
ENV PYTORCH_NO_CUDA=1
ENV FORCE_CUDA=0

# Instala torch SIN CUDA antes de cualquier otra cosa
RUN pip install --no-cache-dir --extra-index-url https://download.pytorch.org/whl/cpu torch torchvision torchaudio

# Evita que Poetry sobreescriba torch con versión de CUDA ( *pip freeze > requirements.txt guarda la versión de torch instalada. *poetry add --lock agrega esta versión al lockfile para que poetry install no la reemplace. )
RUN poetry run pip freeze > requirements.txt && poetry add --lock --no-interaction --no-cache torch torchvision torchaudio

# Instala las dependencias del proyecto sin caché
RUN poetry install --no-root --no-cache --no-interaction

# Copia el resto de los archivos del proyecto (Origen (.) →directorio donde está el Dockerfile; Destino (/app) → la carpeta dentro del contenedor Docker donde se copiarán los archivos.)
COPY . /app

# Expone el puerto 8000
EXPOSE 8000

# Comando para ejecutar la API
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
