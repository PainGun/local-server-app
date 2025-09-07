"""
Servidor Call Of The NIGHT - Punto de entrada principal
"""
from flask import Flask
from config import Config, HOST, PORT, DEBUG, CAPITULOS_PATH
from utils import get_local_ip, obtener_archivos_video, obtener_carpetas
from routes import register_routes

def create_app():
    """
    Factory function para crear la aplicación Flask
    """
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Registrar todas las rutas
    register_routes(app)
    
    return app

def print_server_info():
    """
    Imprimir información del servidor al iniciar
    """
    ip_local = get_local_ip()
    archivos_count = len(obtener_archivos_video())
    carpetas = obtener_carpetas()
    
    print(f"\n🎬 Servidor Call Of The NIGHT iniciado!")
    print(f"📡 IP Local: {ip_local}")
    print(f"🌐 Acceso desde TV: http://{ip_local}:{PORT}")
    print(f"💻 Acceso local: http://localhost:{PORT}")
    print(f"📁 Ruta de archivos: {CAPITULOS_PATH}")
    print(f"\n📋 Archivos encontrados: {archivos_count} archivos de video")
    print(f"📁 Carpetas encontradas: {carpetas}")
    print(f"\n⚡ Servidor ejecutándose... Presiona Ctrl+C para detener")

if __name__ == '__main__':
    # Crear la aplicación
    app = create_app()
    
    # Mostrar información del servidor
    print_server_info()
    
    # Ejecutar servidor
    app.run(
        host=HOST, 
        port=PORT, 
        debug=DEBUG
    )