from collections import defaultdict
import json

# Funcion para mapear los hablantes
def map_diarization_to_speakers(diarization_annotation):

    """
    Procesa la salida de diarización para crear un mapeo de hablantes con sus segmentos de tiempo correspondientes.

    Parámetros:
        diarization_annotation (pyannote.core.Annotation): Anotación de salida de la diarización

    Devuelve:
        list: Una lista de diccionarios con las siguientes claves:
            segment_id (int): ID único para cada segmento
            begin_time (float): Tiempo de inicio del segmento
            end_time (float): Tiempo de fin del segmento
            speaker (str): Etiqueta del hablante para el segmento
    """

    speaker_mapping = {}  # Mapear SPEAKER_X a speaker_01, speaker_02...
    speaker_counter = 1
    processed_segments = []

    for i, (segment, label, confidence) in enumerate(diarization_annotation.itertracks(yield_label=True)):

        start_time, end_time = segment.start, segment.end
        processed_segments.append({
            "segment_id": i,
            "begin_time": round(start_time, 3),  # Formato más preciso
            "end_time": round(end_time, 3),
            "speaker": confidence
        })
    return processed_segments

# Función para procesar la salida del ASR (reconocimiento automático de voz)
def process_asr_output(asr_data):
    """
    Procesa la salida del ASR para extraer los segmentos de transcripci n.

    Par metros:
        asr_data (dict): Diccionario con la informaci n de la transcripci n

    Devuelve:
        list: Una lista de diccionarios con las siguientes claves:
            segment_id (int): ID nico para cada segmento
            text (str): Texto transcripci n para el segmento
            start (float): Tiempo de inicio del segmento
            end (float): Tiempo de fin del segmento
    """
    return asr_data['segments']

# Función para asignar hablantes a los segmentos de transcripción
def assign_speakers_to_transcriptions(trans_segments, speaker_segments):
    """
    Asigna los hablantes a los segmentos de transcripción, encontrando
    el hablante que coincide con el rango de tiempo del segmento.

    Parámetros:
        trans_segments (list): Segmentos de transcripción con la clave 'start' y 'end'.
        speaker_segments (list): Segmentos de diarización con la clave 'begin_time' y 'end_time' y 'speaker'.
    
    Devuelve:
        list: La lista de segmentos de transcripción con la clave 'speaker' agregada.
    """
    for trans in trans_segments:
        trans_start = trans['start']
        trans_end = trans['end']
        trans['speaker'] = None


        for speaker in speaker_segments:
            if speaker['begin_time'] <= trans_start < speaker['end_time'] or \
               speaker['begin_time'] < trans_end <= speaker['end_time']:
                trans['speaker'] = speaker['speaker']
                break
    return trans_segments

# Paso principal del procesamiento
def map_diarization(diarization, result):
    
    """
    Función principal para mapear los hablantes a los segmentos de transcripción.

    Parámetros:
        diarization (pyannote.core.Annotation): Anotación de diarización
        result (dict): Diccionario con la información de la transcripción

    Devuelve:
        list: Una lista de diccionarios con las siguientes claves:
            id (int): ID único para cada segmento
            timestamp (dict): Diccionario con las claves 'start' y 'end' para el rango de tiempo del segmento
            speakerId (str): Etiqueta del hablante para el segmento
            text (str): Texto transcripción para el segmento
    """
    processed_segments = map_diarization_to_speakers(diarization)
    transcription_segments = process_asr_output(result)
    updated_transcriptions = assign_speakers_to_transcriptions(transcription_segments, processed_segments)
    
    # Prepara los datos para la salida en formato JSON
    transcription_w_speakers_data = []

    for trans in updated_transcriptions:
        transcription_w_speakers_data.append({
            "id": trans['id'],
            "timestamp": {"start": trans['start'], "end": trans['end']},
            "speakerId": trans['speaker'],
            "text": trans['text']
        })
    return transcription_w_speakers_data
