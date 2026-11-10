FROM python:3.11.5-slim

RUN apt-get update && apt-get upgrade -y && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

ENV WHISPER_CACHE=/models/whisper
ENV TORCH_HOME=/models/torch
ENV PYANNOTE_CACHE=/models/pyannote

# Crear carpetas de cache persistentes
RUN mkdir -p $WHISPER_CACHE $TORCH_HOME $PYANNOTE_CACHE

WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

# Usar las variables de entorno para setear los paths
ENV XDG_CACHE_HOME=/models
RUN python preload_models.py

EXPOSE 8000
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]