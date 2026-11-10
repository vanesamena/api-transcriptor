# 🗣️ Audio Diarization & Transcription Pipeline

Este proyecto permite realizar **transcripción automática** y **diarización de hablantes** en archivos de audio utilizando [Whisper](https://github.com/openai/whisper) y [PyAnnote](https://github.com/pyannote/pyannote-audio).

---

## 🚀 ¿Qué hace?

Dado un archivo de audio:

1. Transcribe el contenido usando Whisper.
2. Identifica los distintos hablantes con PyAnnote.
3. Devuelve un JSON con el texto atribuido a cada persona que habla.

---

## 📦 Requisitos

- Python 3.11
- Token de Hugging Face válido para acceder al modelo de diarización

---

## 🛠 Instalación

### 1. Crear ambiente
```bash
python virtualenv .env_whisper
.env_whisper\\Scripts\\activate  # o  source .env_whisper/bin/activate en ubuntu
```
### 2. Instalar dependencias
```bash
pip install --upgrade pip
pip install -r requirements.txt
```
---

## 🔐 Configuración

En el archivo `.env` en la raíz del proyecto configura token de Hugging Face:

```env
HF_AUTH_TOKEN=tu_token_personal
```

---

## ▶️ Uso

### En terminal

1. Transcripción y diarización básica
```bash
python main.py --audio_path /ruta/al/audio.wav
```
2. Especificar cantidad de hablantes (por ejemplo, 3)
```bash
python main.py --audio_path /ruta/al/audio.wav --num_speakers 3
```
3. Usar un modelo específico de Whisper (por ejemplo, medium) (por defecto esta turbo)
```bash
python main.py --audio_path /ruta/al/audio.wav --model medium
```
4. Cambiar el idioma del audio (por ejemplo, inglés)
```bash
python main.py --audio_path /ruta/al/audio.wav --language en
```
5. Guardar la salida como archivo JSON

```bash
python main.py --audio_path /ruta/audio.wav --output resultado.json
```

### En notebook
- Abrir [whisper_diarization.ipynb](whisper_diarization.ipynb)
- Configurar el path del archivo y correr la celda
- Si se desea almacenar el json de salida, configurarlo tambien en la celda 
---

## 🧪 Salida esperada

```json
[
  {
    "id": 0,
    "timestamp": {
      "start": 1.32,
      "end": 13.28
    },
    "speaker": "SPEAKER_00",
    "text": "Hola, ¿cómo estás?"
  },
  {
     "id": 1,
    "timestamp": {
      "start": 17.74,
      "end": 23.48
    },
    "speaker": "SPEAKER_01",
    "text": "Bien, gracias. ¿Y vos?"
  }
]
```

---

## 📁 Archivos principales

- `main.py`: Script principal para ejecutar el pipeline
- `pipeline.py`: Funciones reutilizables para transcripción y diarización
- `map_diarization`: Funciones de mapeo de la diarización
- `.env`: Donde definir tu token de Hugging Face
- `requirements.txt`: Dependencias del proyecto

---

## 🧠 Modelos usados

- **Whisper**: `turbo` (puede cambiarse a `small`, `medium`, etc.)
- **Diarización**: `pyannote/speaker-diarization-3.1`

---





# 🧠 API de Transcripción y Diarización

Esta API recibe un archivo de audio y devuelve la transcripción junto con los segmentos de voz clasificados por hablante. Utiliza Whisper para transcripción y Pyannote para diarización.


## 🚀 ¿Cómo levantar la API?

1. **Ejecutar el servidor FastAPI:**
   ```bash
   uvicorn api:app --reload
   ```
2. **Acceder a la documentación interactiva:**
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

## 📥 Endpoint principal

#### `POST /process-audio/`
Procesa un archivo de audio y devuelve la transcripción y los segmentos de voz por hablante.

### 🔧 Parámetros (form-data):
| Nombre         | Tipo    | Requerido | Descripción                                            |
| -------------- | ------- | --------- | ------------------------------------------------------ |
| `audio_file`   | Archivo | ✅         | Archivo de audio en formato `.wav`, `.mp3`, etc.       |
| `num_speakers` | Entero  | ❌         | Número estimado de hablantes en el audio               |
| `language`     | Enum    | ❌         | Idioma del audio (`es`, `en`, `pt`) - por defecto `es` |
| `model`        | Enum    | ❌         | Modelo Whisper a usar (`base`, `small`, `turbo`, etc.) |

### 📤 Respuesta (200 OK)
```json
[
  {
    "id": 0,
    "timestamp": {
      "start": 1.34,
      "end": 13.28
    },
    "speakerId": "SPEAKER_01",
    "text": "Hola, ¿cómo estás?"
  },
  {
    "id": 1,
    "timestamp": {
      "start": 17.74,
      "end": 23.48
    },
    "speakerId": "SPEAKER_01",
    "text": "Bien, gracias. ¿Y vos?"
  }
]
```

## 🐍 Ejemplo de uso desde Python
```python
import requests

url = "http://localhost:8000/process-audio/"
audio_path = "ruta/a/tu_audio.mp3"  # Cambiar por tu archivo local

with open(audio_path, "rb") as f:
    files = {"audio_file": f}
    data = {
        "num_speakers": 2,
        "language": "es",
        "model": "turbo"
    }
    response = requests.post(url, files=files, data=data)

# Ver resultado
if response.ok:
    print("✅ Resultado:")
    print(response.json())
else:
    print("❌ Error:", response.status_code)
    print(response.text)
```
NOTA: Asegurate de que la API esté corriendo en localhost:8000 antes de ejecutar este script.
---


# 🐳 Uso con Docker

Esta sección explica cómo construir y correr la API usando Docker.

---

### 🔨 Build de la imagen

Desde la raíz del proyecto (donde está el `Dockerfile` y `requirements.txt`), ejecutá:

```bash
docker build -t transcripcion-api .
```
Esto va a construir la imagen Docker con todas las dependencias necesarias.

🛑 Tip adicional
Si hacés cambios en tu código y necesitás reconstruir la imagen, podés hacerlo con --no-cache:
```bash
docker build --no-cache -t transcripcion-api .
```

### ▶️ Correr la API en un contenedor

Una vez construida la imagen, parado en el mismo lugar, ejecutá:
```bash
docker run -p 8000:8000 transcripcion-api
```
Esto expone la API en `http://localhost:8000`.

### 📖 Acceder a la documentación
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)


**NOTA: Para pegarle a la api desde python se puede usar el mismo codigo de mas arriba**
Para usar docker descargar Docker Desktop: 👉 [https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/)