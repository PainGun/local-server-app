"""
Configuración del servidor Call Of The NIGHT
"""
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde archivo .env
load_dotenv()

# Configuración del servidor
HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 5000))
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'

# Ruta donde están los capítulos
CAPITULOS_PATH = os.getenv('VIDEO_PATH', r"D:\Mis Documentos\Call Of The NIGHT")

# Configuración de auto-avance
AUTO_ADVANCE_TRIGGER_SECONDS = int(os.getenv('AUTO_ADVANCE_TRIGGER_SECONDS', 100))
AUTO_ADVANCE_COUNTDOWN_SECONDS = int(os.getenv('AUTO_ADVANCE_COUNTDOWN_SECONDS', 15))

# Configuración de progreso
PROGRESS_SAVE_INTERVAL = int(os.getenv('PROGRESS_SAVE_INTERVAL', 10))

# Configuración de thumbnails
THUMBNAIL_CACHE_DIR = os.getenv('THUMBNAIL_CACHE_DIR', 'thumbnails_cache')

# Extensiones de video soportadas
VIDEO_EXTENSIONS = [
    '*.mp4', '*.avi', '*.mkv', '*.mov', '*.wmv', 
    '*.flv', '*.webm', '*.m4v', '*.3gp'
]

# Configuración de la aplicación Flask
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    CAPITULOS_PATH = CAPITULOS_PATH