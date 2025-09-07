"""
Rutas del servidor Call Of The NIGHT
"""
import os
from flask import render_template_string, send_file, send_from_directory
from config import CAPITULOS_PATH
from utils import get_local_ip, obtener_archivos_video, obtener_archivos_video_carpeta, obtener_carpetas
from templates import HTML_TEMPLATE
from video_player_template import VIDEO_PLAYER_TEMPLATE
from thumbnails import get_thumbnail_base64, get_video_duration, format_duration, regenerate_all_thumbnails
from progress import get_video_progress, get_all_progress, update_video_progress, get_progress_stats
from config import AUTO_ADVANCE_TRIGGER_SECONDS, AUTO_ADVANCE_COUNTDOWN_SECONDS, APP_TITLE

def register_routes(app):
    """
    Registrar todas las rutas en la aplicación Flask
    """
    
    @app.route('/')
    def index():
        ip_local = get_local_ip()
        return render_template_string(HTML_TEMPLATE, 
                                    ip_local=ip_local,
                                    ruta_capitulos=CAPITULOS_PATH,
                                    obtener_archivos_video=obtener_archivos_video,
                                    obtener_archivos_video_carpeta=obtener_archivos_video_carpeta,
                                    obtener_carpetas=obtener_carpetas,
                                    app_title=APP_TITLE)

    @app.route('/ver/<archivo>')
    def ver_video_principal(archivo):
        """Servir archivo directamente de la carpeta principal"""
        archivo_path = os.path.join(CAPITULOS_PATH, archivo)
        if os.path.exists(archivo_path):
            return send_file(archivo_path)
        else:
            return "Archivo no encontrado", 404

    @app.route('/ver/<carpeta>/<archivo>')
    def ver_video_carpeta(carpeta, archivo):
        """Servir archivo de una subcarpeta"""
        archivo_path = os.path.join(CAPITULOS_PATH, carpeta, archivo)
        if os.path.exists(archivo_path):
            return send_file(archivo_path)
        else:
            return "Archivo no encontrado", 404

    @app.route('/api/archivos')
    def api_archivos_principales():
        return {'archivos': obtener_archivos_video()}

    @app.route('/api/carpetas')
    def api_carpetas():
        return {'carpetas': obtener_carpetas()}

    @app.route('/api/archivos/<carpeta>')
    def api_archivos_carpeta(carpeta):
        archivos = obtener_archivos_video_carpeta(carpeta)
        return {'archivos': archivos}

    @app.route('/thumbnail/<path:filename>')
    def serve_thumbnail(filename):
        """Servir archivos de miniatura"""
        from thumbnails import THUMBNAILS_DIR
        return send_from_directory(THUMBNAILS_DIR, filename)

    @app.route('/api/thumbnail/<path:video_path>')
    def get_thumbnail_api(video_path):
        """API para obtener miniatura de video"""
        full_video_path = os.path.join(CAPITULOS_PATH, video_path)
        if os.path.exists(full_video_path):
            thumbnail_base64 = get_thumbnail_base64(full_video_path)
            duration = get_video_duration(full_video_path)
            return {
                'thumbnail': thumbnail_base64,
                'duration': format_duration(duration)
            }
        return {'error': 'Video not found'}, 404

    @app.route('/player/<path:video_path>')
    def video_player(video_path):
        """Reproductor de video en pantalla completa"""
        full_video_path = os.path.join(CAPITULOS_PATH, video_path)
        
        if not os.path.exists(full_video_path):
            return "Video no encontrado", 404
        
        # Obtener lista de todos los videos para navegación
        all_videos = []
        
        # Videos de la carpeta principal
        archivos_principales = obtener_archivos_video()
        for archivo in archivos_principales:
            all_videos.append({
                'name': archivo,
                'path': archivo,
                'full_path': os.path.join(CAPITULOS_PATH, archivo)
            })
        
        # Videos de subcarpetas
        carpetas = obtener_carpetas()
        for carpeta in carpetas:
            archivos = obtener_archivos_video_carpeta(carpeta)
            for archivo in archivos:
                all_videos.append({
                    'name': archivo,
                    'path': f"{carpeta}/{archivo}",
                    'full_path': os.path.join(CAPITULOS_PATH, carpeta, archivo)
                })
        
        # Ordenar todos los videos por número de capítulo
        def extract_number(video_info):
            import re
            match = re.search(r'cap(\d+)', video_info['name'], re.IGNORECASE)
            return int(match.group(1)) if match else 0
        
        all_videos.sort(key=extract_number)
        
        # Encontrar el índice del video actual
        current_index = -1
        for i, video in enumerate(all_videos):
            if video['path'] == video_path:
                current_index = i
                break
        
        if current_index == -1:
            return "Video no encontrado en la lista", 404
        
        # Crear URL del video
        video_url = f"/ver/{video_path}"
        
        # Renderizar el reproductor
        return render_template_string(VIDEO_PLAYER_TEMPLATE,
                                    video_name=os.path.basename(video_path),
                                    video_url=video_url,
                                    video_index=current_index,
                                    total_videos=len(all_videos),
                                    video_list=all_videos,
                                    auto_advance_trigger_seconds=AUTO_ADVANCE_TRIGGER_SECONDS,
                                    auto_advance_countdown_seconds=AUTO_ADVANCE_COUNTDOWN_SECONDS,
                                    app_title=APP_TITLE)

    @app.route('/api/regenerate-thumbnails')
    def regenerate_thumbnails_api():
        """API para regenerar todas las miniaturas"""
        try:
            regenerated_count = regenerate_all_thumbnails()
            return {
                'success': True,
                'message': f'Se regeneraron {regenerated_count} miniaturas',
                'count': regenerated_count
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Error regenerando miniaturas: {str(e)}'
            }, 500

    @app.route('/api/progress/<path:video_path>')
    def get_progress_api(video_path):
        """API para obtener el progreso de un video"""
        try:
            progress = get_video_progress(video_path)
            return {
                'success': True,
                'progress': progress
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Error obteniendo progreso: {str(e)}'
            }, 500

    @app.route('/api/progress', methods=['POST'])
    def update_progress_api():
        """API para actualizar el progreso de un video"""
        try:
            from flask import request
            data = request.get_json()
            
            video_name = data.get('video_name')
            current_time = data.get('current_time', 0)
            duration = data.get('duration', 0)
            is_completed = data.get('is_completed', False)
            
            if not video_name:
                return {
                    'success': False,
                    'message': 'Nombre de video requerido'
                }, 400
            
            progress = update_video_progress(video_name, current_time, duration, is_completed)
            
            return {
                'success': True,
                'progress': progress
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Error actualizando progreso: {str(e)}'
            }, 500

    @app.route('/api/progress/all')
    def get_all_progress_api():
        """API para obtener todo el progreso de visualización"""
        try:
            progress_data = get_all_progress()
            stats = get_progress_stats()
            return {
                'success': True,
                'progress': progress_data,
                'stats': stats
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Error obteniendo progreso: {str(e)}'
            }, 500
