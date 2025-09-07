"""
Módulo para generar y manejar miniaturas de video
"""
import os
import cv2
import hashlib
from PIL import Image
import io
import base64
from config import CAPITULOS_PATH

# Carpeta para almacenar miniaturas
THUMBNAILS_DIR = "thumbnails"

def ensure_thumbnails_dir():
    """Crear directorio de miniaturas si no existe"""
    if not os.path.exists(THUMBNAILS_DIR):
        os.makedirs(THUMBNAILS_DIR)

def get_thumbnail_path(video_path):
    """Obtener la ruta de la miniatura para un video"""
    ensure_thumbnails_dir()
    
    # Crear hash único basado en la ruta del video
    video_hash = hashlib.md5(video_path.encode()).hexdigest()
    return os.path.join(THUMBNAILS_DIR, f"{video_hash}.jpg")

def generate_thumbnail(video_path, thumbnail_path, time_seconds=None):
    """
    Generar miniatura de video usando OpenCV con frame aleatorio
    """
    try:
        # Abrir el video
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            return False
        
        # Obtener duración total del video
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        duration = frame_count / fps if fps > 0 else 0
        
        if duration == 0:
            cap.release()
            return False
        
        # Si no se especifica tiempo, usar un tiempo aleatorio entre 10% y 80% del video
        if time_seconds is None:
            import hashlib
            # Usar hash del nombre del archivo para generar un tiempo consistente pero variado
            file_hash = hashlib.md5(video_path.encode()).hexdigest()
            # Convertir hash a número entre 0 y 1
            hash_ratio = int(file_hash[:8], 16) / 0xffffffff
            # Mapear a tiempo entre 10% y 80% de la duración
            time_seconds = (0.1 + hash_ratio * 0.7) * duration
        else:
            # Asegurar que el tiempo no exceda la duración
            time_seconds = min(time_seconds, duration * 0.9)
        
        # Obtener el frame en el tiempo especificado
        cap.set(cv2.CAP_PROP_POS_MSEC, time_seconds * 1000)
        ret, frame = cap.read()
        
        if not ret:
            # Si no se puede obtener el frame en el tiempo especificado, intentar con otros tiempos
            fallback_times = [duration * 0.25, duration * 0.5, duration * 0.75, 0]
            for fallback_time in fallback_times:
                cap.set(cv2.CAP_PROP_POS_MSEC, fallback_time * 1000)
                ret, frame = cap.read()
                if ret:
                    break
        
        cap.release()
        
        if ret:
            # Redimensionar la imagen
            height, width = frame.shape[:2]
            if width > 400:
                ratio = 400 / width
                new_width = 400
                new_height = int(height * ratio)
                frame = cv2.resize(frame, (new_width, new_height))
            
            # Guardar la miniatura
            cv2.imwrite(thumbnail_path, frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
            return True
        
        return False
        
    except Exception as e:
        print(f"Error generando miniatura para {video_path}: {e}")
        return False

def get_or_create_thumbnail(video_path):
    """
    Obtener miniatura existente o crear una nueva
    """
    thumbnail_path = get_thumbnail_path(video_path)
    
    # Si la miniatura ya existe, devolverla
    if os.path.exists(thumbnail_path):
        return thumbnail_path
    
    # Generar nueva miniatura
    if generate_thumbnail(video_path, thumbnail_path):
        return thumbnail_path
    
    return None

def get_thumbnail_base64(video_path):
    """
    Obtener miniatura como base64 para usar directamente en HTML
    """
    thumbnail_path = get_or_create_thumbnail(video_path)
    
    if thumbnail_path and os.path.exists(thumbnail_path):
        try:
            with open(thumbnail_path, 'rb') as img_file:
                img_data = img_file.read()
                base64_data = base64.b64encode(img_data).decode('utf-8')
                return f"data:image/jpeg;base64,{base64_data}"
        except Exception as e:
            print(f"Error leyendo miniatura {thumbnail_path}: {e}")
    
    return None

def get_video_duration(video_path):
    """
    Obtener duración del video en segundos
    """
    try:
        cap = cv2.VideoCapture(video_path)
        if cap.isOpened():
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
            duration = frame_count / fps if fps > 0 else 0
            cap.release()
            return duration
        return 0
    except:
        return 0

def format_duration(seconds):
    """
    Formatear duración en formato HH:MM:SS
    """
    if seconds == 0:
        return "00:00"
    
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    else:
        return f"{minutes:02d}:{secs:02d}"

def regenerate_all_thumbnails():
    """
    Regenerar todas las miniaturas existentes con nuevos tiempos aleatorios
    """
    import glob
    from config import CAPITULOS_PATH, VIDEO_EXTENSIONS
    
    ensure_thumbnails_dir()
    
    # Obtener todos los archivos de video
    all_videos = []
    for extension in VIDEO_EXTENSIONS:
        all_videos.extend(glob.glob(os.path.join(CAPITULOS_PATH, extension)))
        all_videos.extend(glob.glob(os.path.join(CAPITULOS_PATH, extension.upper())))
    
    # Obtener carpetas
    carpetas = []
    if os.path.exists(CAPITULOS_PATH):
        for item in os.listdir(CAPITULOS_PATH):
            item_path = os.path.join(CAPITULOS_PATH, item)
            if os.path.isdir(item_path):
                carpetas.append(item)
    
    # Agregar videos de subcarpetas
    for carpeta in carpetas:
        for extension in VIDEO_EXTENSIONS:
            all_videos.extend(glob.glob(os.path.join(CAPITULOS_PATH, carpeta, extension)))
            all_videos.extend(glob.glob(os.path.join(CAPITULOS_PATH, carpeta, extension.upper())))
    
    # Eliminar duplicados
    all_videos = list(set(all_videos))
    
    # Función para extraer el número del capítulo
    def extract_number(filename):
        import re
        match = re.search(r'cap(\d+)', filename, re.IGNORECASE)
        return int(match.group(1)) if match else 0
    
    # Ordenar por número de capítulo (cap1, cap2, ..., cap10, cap11, etc.)
    all_videos.sort(key=lambda x: extract_number(os.path.basename(x)))
    
    print(f"Regenerando {len(all_videos)} miniaturas...")
    
    regenerated = 0
    for video_path in all_videos:
        thumbnail_path = get_thumbnail_path(video_path)
        # Eliminar miniatura existente si existe
        if os.path.exists(thumbnail_path):
            os.remove(thumbnail_path)
        
        # Generar nueva miniatura
        if generate_thumbnail(video_path, thumbnail_path):
            regenerated += 1
            print(f"✓ Regenerada: {os.path.basename(video_path)}")
        else:
            print(f"✗ Error: {os.path.basename(video_path)}")
    
    print(f"Miniaturas regeneradas: {regenerated}/{len(all_videos)}")
    return regenerated
