import json
import os
from datetime import datetime

# Archivo para almacenar el progreso de visualización
PROGRESS_FILE = os.path.join(os.getcwd(), 'viewing_progress.json')

def ensure_progress_file():
    """Asegurar que el archivo de progreso existe"""
    if not os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
            json.dump({}, f, ensure_ascii=False, indent=2)

def load_progress():
    """Cargar el progreso de visualización desde el archivo"""
    ensure_progress_file()
    try:
        with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}

def save_progress(progress_data):
    """Guardar el progreso de visualización en el archivo"""
    ensure_progress_file()
    with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
        json.dump(progress_data, f, ensure_ascii=False, indent=2)

def update_video_progress(video_name, current_time, duration, is_completed=False):
    """
    Actualizar el progreso de un video específico
    
    Args:
        video_name (str): Nombre del archivo de video
        current_time (float): Tiempo actual en segundos
        duration (float): Duración total en segundos
        is_completed (bool): Si el video fue completado
    """
    progress_data = load_progress()
    
    # Calcular porcentaje de progreso
    if duration > 0:
        progress_percentage = min(100, (current_time / duration) * 100)
    else:
        progress_percentage = 0
    
    # Marcar como completado si se ve más del 90% o si se especifica
    if progress_percentage >= 90 or is_completed:
        is_completed = True
        progress_percentage = 100
    
    # Actualizar datos del video
    progress_data[video_name] = {
        'current_time': current_time,
        'duration': duration,
        'progress_percentage': progress_percentage,
        'is_completed': is_completed,
        'last_watched': datetime.now().isoformat(),
        'watch_count': progress_data.get(video_name, {}).get('watch_count', 0) + 1
    }
    
    save_progress(progress_data)
    return progress_data[video_name]

def get_video_progress(video_name):
    """
    Obtener el progreso de un video específico
    
    Returns:
        dict: Datos de progreso del video o None si no existe
    """
    progress_data = load_progress()
    return progress_data.get(video_name)

def get_all_progress():
    """Obtener todo el progreso de visualización"""
    return load_progress()

def mark_video_completed(video_name):
    """Marcar un video como completado"""
    progress_data = load_progress()
    if video_name in progress_data:
        progress_data[video_name]['is_completed'] = True
        progress_data[video_name]['progress_percentage'] = 100
        progress_data[video_name]['last_watched'] = datetime.now().isoformat()
        save_progress(progress_data)

def reset_video_progress(video_name):
    """Resetear el progreso de un video específico"""
    progress_data = load_progress()
    if video_name in progress_data:
        del progress_data[video_name]
        save_progress(progress_data)

def reset_all_progress():
    """Resetear todo el progreso de visualización"""
    save_progress({})

def get_progress_stats():
    """Obtener estadísticas del progreso de visualización"""
    progress_data = load_progress()
    
    total_videos = len(progress_data)
    completed_videos = sum(1 for video in progress_data.values() if video.get('is_completed', False))
    in_progress_videos = sum(1 for video in progress_data.values() 
                           if not video.get('is_completed', False) and video.get('progress_percentage', 0) > 0)
    
    return {
        'total_videos': total_videos,
        'completed_videos': completed_videos,
        'in_progress_videos': in_progress_videos,
        'not_started_videos': total_videos - completed_videos - in_progress_videos
    }
