from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, validator
from enum import Enum
from typing import Optional
from pipeline import process_audio
import tempfile
import shutil
import os

class LanguageEnum(str, Enum):
    es = "es"
    en = "en"
    pt = "pt"

class ModelEnum(str, Enum):
    base = "base"
    small = "small"
    medium = "medium"
    large = "large"
    turbo = "turbo"

app = FastAPI(
    title="🧠 API de Transcripción y Diarización",
    description="Subí un archivo de audio y obtené la transcripción junto con los segmentos por hablante.",
    version="1.0.0"
)

@app.post(
    "/process-audio/",
    summary="Procesar audio (transcripción + diarización)",
    description="Recibe un archivo de audio y parámetros opcionales para devolver la transcripción y los segmentos de cada hablante."
)
async def transcribe_audio(
    audio_file: UploadFile = File(..., description="Archivo de audio (.wav, .mp3, etc)"),
    num_speakers: Optional[int] = None,
    language: LanguageEnum = Form(LanguageEnum.es, description="Idioma del audio (por defecto: 'es')"),
    model: ModelEnum = Form(ModelEnum.turbo, description="Modelo Whisper a usar (por defecto: 'turbo')")
):
    # Validación adicional
    if num_speakers is not None and int(num_speakers) <= 0:
        return JSONResponse(content={"error": "El número de hablantes debe ser mayor que cero."}, status_code=400)

    # Guardar temporalmente el archivo
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(audio_file.filename)[1]) as tmp:
        shutil.copyfileobj(audio_file.file, tmp)
        tmp_path = tmp.name

    try:
        # Ejecutar pipeline
        result = process_audio(
            audio_path=tmp_path,
            num_speakers=num_speakers,
            language=language,
            model_name=model
        )
        return JSONResponse(content=result, status_code=200)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

    finally:
        os.remove(tmp_path)
