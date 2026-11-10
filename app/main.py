# main.py
import argparse
import json
from pipeline import process_audio

def main():
    """
    Entrada principal del programa. Lee los argumentos de la linea de comandos y
    procesa el audio especificado en el path para obtener la transcripci n y diarizaci n.

    Parmetros:
        --audio_path: Ruta al archivo de audio de entrada (.wav, .mp3, etc)
        --num_speakers: Cantidad de hablantes a diarizar (opcional)
        --output: Ruta para guardar el resultado en formato JSON (opcional)
        --language: Idioma del audio (por defecto: es)
        --model: Nombre del modelo Whisper a usar (por defecto: turbo)

    El resultado se imprime en la consola en formato JSON. Si se especifica la
    opcion --output, se guarda el resultado en el archivo especificado.
    """
    parser = argparse.ArgumentParser(description="Transcribe y diariza un archivo de audio.")
    parser.add_argument("--audio_path", required=True, help="Ruta al archivo de audio de entrada (.wav, .mp3, etc)")
    parser.add_argument("--num_speakers", type=int, help="Cantidad de hablantes a diarizar (opcional)")
    parser.add_argument("--output", help="Ruta para guardar el resultado en formato JSON (opcional)")
    parser.add_argument("--language", default="es", help="Idioma del audio (por defecto: es)")
    parser.add_argument("--model", default="turbo", help="Nombre del modelo Whisper a usar (por defecto: turbo)")

    args = parser.parse_args()

    print("🎙️ Procesando audio...")
    print(f"num_speakers: {args.num_speakers} | model: {args.model} | language: {args.language}")

    result = process_audio(
        audio_path=args.audio_path,
        num_speakers=args.num_speakers,
        language=args.language,
        model_name=args.model
    )

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=4, ensure_ascii=False)
        print(f"✅ Resultado guardado en: {args.output}")
    else:
        print(json.dumps(result, indent=4, ensure_ascii=False))

if __name__ == "__main__":
    main()
