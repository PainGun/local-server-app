"""
Utilidades para el servidor Call Of The NIGHT
"""
import os
import glob
import socket
from config import CAPITULOS_PATH, VIDEO_EXTENSIONS

def get_local_ip():
    """
    Obtener la IP local del servidor
    """
    try:
        # Conectar a una dirección externa para obtener la IP local
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def obtener_archivos_video():
    """
    Función para obtener todos los archivos de video de la carpeta principal
    """
    if not os.path.exists(CAPITULOS_PATH):
        return []
    
    archivos = []
    
    for extension in VIDEO_EXTENSIONS:
        archivos.extend(glob.glob(os.path.join(CAPITULOS_PATH, extension)))
        archivos.extend(glob.glob(os.path.join(CAPITULOS_PATH, extension.upper())))
    
    # Eliminar duplicados y ordenar archivos por número de capítulo
    archivos = list(set(archivos))  # Eliminar duplicados
    
    # Función para extraer el número del capítulo
    def extract_number(filename):
        import re
        match = re.search(r'cap(\d+)', filename, re.IGNORECASE)
        return int(match.group(1)) if match else 0
    
    # Ordenar por número de capítulo (cap1, cap2, ..., cap10, cap11, etc.)
    archivos.sort(key=lambda x: extract_number(os.path.basename(x)))
    return [os.path.basename(archivo) for archivo in archivos]

def obtener_archivos_video_carpeta(carpeta):
    """
    Función para obtener archivos de video de una subcarpeta (si existe)
    """
    carpeta_path = os.path.join(CAPITULOS_PATH, carpeta)
    if not os.path.exists(carpeta_path):
        return []
    
    archivos = []
    
    for extension in VIDEO_EXTENSIONS:
        archivos.extend(glob.glob(os.path.join(carpeta_path, extension)))
        archivos.extend(glob.glob(os.path.join(carpeta_path, extension.upper())))
    
    # Eliminar duplicados y ordenar archivos por número de capítulo
    archivos = list(set(archivos))  # Eliminar duplicados
    
    # Función para extraer el número del capítulo
    def extract_number(filename):
        import re
        match = re.search(r'cap(\d+)', filename, re.IGNORECASE)
        return int(match.group(1)) if match else 0
    
    # Ordenar por número de capítulo (cap1, cap2, ..., cap10, cap11, etc.)
    archivos.sort(key=lambda x: extract_number(os.path.basename(x)))
    return [os.path.basename(archivo) for archivo in archivos]

def obtener_carpetas():
    """
    Función para obtener lista de carpetas (capítulos)
    """
    carpetas = []
    if os.path.exists(CAPITULOS_PATH):
        for item in os.listdir(CAPITULOS_PATH):
            item_path = os.path.join(CAPITULOS_PATH, item)
            if os.path.isdir(item_path):
                carpetas.append(item)
        
        # Función para extraer el número del capítulo de carpetas
        def extract_number(filename):
            import re
            match = re.search(r'cap(\d+)', filename, re.IGNORECASE)
            return int(match.group(1)) if match else 0
        
        # Ordenar por número de capítulo (cap1, cap2, ..., cap10, cap11, etc.)
        carpetas.sort(key=lambda x: extract_number(x))
    return carpetas
