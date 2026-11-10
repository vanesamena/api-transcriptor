import whisper
import torch
from pyannote.audio import Pipeline
from map_diarization import map_diarization
import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "../.env"))

# Función para cargar el modelo Whisper
def load_whisper_model(model_name="turbo"):
    """
    Carga el modelo Whisper especificado por el nombre del modelo.

    Parámetros:
        model_name (str): El nombre del modelo Whisper a cargar. Por defecto es "turbo".

    Retorna:
        tuple: Una tupla que contiene el modelo cargado y el dispositivo en el que está cargado ("cuda" o "cpu").
    """

    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = whisper.load_model(model_name, device=device)
    print(f"Modelo {model_name} cargado en {device}")
    return model, device

# Función para transcribir el audio usando Whisper
def transcribe_audio_whisper(model, audio_path, language="es"):
    """
    Transcribe el audio especificado en el path usando el modelo Whisper cargado.

    Parámetros:
        model (whisper.Model): El modelo Whisper cargado.
        audio_path (str): La ruta del archivo de audio a transcribir.
        language (str): El idioma del audio. Por defecto es "es".

    Retorna:
        whisper.Result: El resultado de la transcripción con las palabras y sus timestamps.
    """
    
    result = model.transcribe(audio_path, language=language, word_timestamps=True)
    return result

# Función para realizar la diarización del audio
def diarize_audio(audio_path, num_speakers = None):
    """
    Realiza la diarización del audio especificado en el path.

    Parámetros:
        audio_path (str): La ruta del archivo de audio a diarizar.
        num_speakers (int, optional): El número de hablantes a detectar. Por defecto es None.

    Retorna:
        pyannote.core.Annotation: La anotación de diarización con los segmentos de habla etiquetados.
    """
    hf_token = os.getenv("HF_AUTH_TOKEN")
    if not hf_token:
        raise EnvironmentError("HF_AUTH_TOKEN no está definido en el entorno ni en el .env")
    
    pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-3.1", use_auth_token=hf_token)
    
    if torch.cuda.is_available():
        diarization.to(torch.device("cuda"))
    else:
        print("CUDA no está disponible, usando CPU")
    if num_speakers:
        diarization = pipeline(audio_path, num_speakers = num_speakers)
    else:
        diarization = pipeline(audio_path)
    return diarization

# Paso principal del procesamiento
# Ejecuta transcripción, diarización y asociación
def process_audio(audio_path, num_speakers=None, model_name="turbo", language="es"):
    """
    Procesa el audio especificado en el path para obtener la transcripción y diarización.

    Parámetros:
        audio_path (str): La ruta del archivo de audio a procesar.
        num_speakers (int, optional): El número de hablantes a detectar. Por defecto es None.
        model_name (str): El nombre del modelo Whisper a utilizar. Por defecto es "turbo".
        language (str): El idioma del audio. Por defecto es "es".

    Retorna:
        list: La lista de segmentos de transcripción con las claves 'speaker', 'start', 'end', 'text'.
    """
    model, _ = load_whisper_model(model_name)
    transcription = transcribe_audio_whisper(model, audio_path, language)
    diarization = diarize_audio(audio_path, num_speakers)
    match = map_diarization(diarization, transcription)
    return match