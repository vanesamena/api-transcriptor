# preload_models.py
import whisper
from pyannote.audio import Pipeline
import os
from dotenv import load_dotenv


try:
    # Cargar variables de entorno
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    if not os.path.exists(env_path):
        raise FileNotFoundError(f"No se encontró el archivo .env en {env_path}")
    
    load_dotenv(env_path)

    # Cargar modelo de Whisper (e.g. tiny, base, small, medium, large-v2, etc.)
    whisper.load_model("turbo")

    # Autenticarse con Hugging Face (usa tu token si es privado)
    HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

    # Cargar pipeline de diarización
    pipeline = Pipeline.from_pretrained(
        "pyannote/speaker-diarization-3.1", use_auth_token=HUGGINGFACE_TOKEN
    )

    # # Hacer una predicción dummy para que baje todos los pesos
    # from pyannote.core import Segment
    # dummy_audio = {"uri": "dummy", "audio": "/dev/null"}
    # pipeline(dummy_audio, num_speakers=2)
except:
    raise
