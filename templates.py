"""
Templates HTML para el servidor Call Of The NIGHT
"""

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ app_title }} - Servidor Local</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
            min-height: 100vh;
            color: #ffffff;
            overflow-x: hidden;
        }
        
        .background-animation {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: 
                radial-gradient(circle at 20% 80%, rgba(120, 119, 198, 0.3) 0%, transparent 50%),
                radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.3) 0%, transparent 50%),
                radial-gradient(circle at 40% 40%, rgba(120, 219, 255, 0.2) 0%, transparent 50%);
            animation: backgroundShift 20s ease-in-out infinite;
            z-index: -1;
        }
        
        @keyframes backgroundShift {
            0%, 100% { transform: translateX(0) translateY(0); }
            33% { transform: translateX(-20px) translateY(-10px); }
            66% { transform: translateX(20px) translateY(10px); }
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
            position: relative;
            z-index: 1;
        }
        
        .header {
            text-align: center;
            margin-bottom: 40px;
            padding: 40px 0;
        }
        
        .header h1 {
            font-size: 3.5rem;
            font-weight: 700;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 10px;
            text-shadow: 0 0 30px rgba(102, 126, 234, 0.5);
        }
        
        .header .subtitle {
            font-size: 1.2rem;
            color: #a0a0a0;
            font-weight: 300;
        }
        
        .server-info {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 25px;
            margin-bottom: 40px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }
        
        .server-info h3 {
            color: #667eea;
            margin-bottom: 15px;
            font-size: 1.3rem;
            font-weight: 600;
        }
        
        .info-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
        }
        
        .info-item {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 10px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 10px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .info-item i {
            color: #667eea;
            font-size: 1.2rem;
        }
        
        .capitulo {
            background: rgba(255, 255, 255, 0.03);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            margin: 30px 0;
            padding: 30px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            transition: all 0.3s ease;
        }
        
        .capitulo:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(102, 126, 234, 0.2);
            border-color: rgba(102, 126, 234, 0.3);
        }
        
        .capitulo h2 {
            color: #ffffff;
            margin-bottom: 25px;
            font-size: 1.8rem;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 15px;
        }
        
        .capitulo h2 i {
            color: #667eea;
            font-size: 1.5rem;
        }
        
        .video-list {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 15px;
        }
        
        .video-item {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 0;
            text-align: center;
            transition: all 0.3s ease;
            cursor: pointer;
            position: relative;
            overflow: hidden;
            aspect-ratio: 16/9;
            max-height: 150px;
        }
        
        .progress-bar {
            position: absolute;
            bottom: 0;
            left: 0;
            height: 6px;
            background: #e50914;
            transition: width 0.3s ease;
            z-index: 10;
            border-radius: 0 0 12px 12px;
            box-shadow: 0 0 10px rgba(229, 9, 20, 0.5);
        }
        
        .progress-bar.completed {
            background: #46d369;
            box-shadow: 0 0 10px rgba(70, 211, 105, 0.5);
        }
        
        .video-status {
            position: absolute;
            top: 8px;
            right: 8px;
            background: rgba(0, 0, 0, 0.7);
            color: white;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.8rem;
            font-weight: 500;
            z-index: 10;
        }
        
        .video-status.completed {
            background: #46d369;
        }
        
        .video-status.in-progress {
            background: #e50914;
        }
        
        .video-item::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
            transition: left 0.5s ease;
        }
        
        .video-item:hover::before {
            left: 100%;
        }
        
        .video-item:hover {
            background: rgba(102, 126, 234, 0.2);
            border-color: #667eea;
            transform: translateY(-5px) scale(1.02);
            box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3);
        }
        
        .video-item a {
            text-decoration: none;
            color: inherit;
            display: block;
            position: relative;
            z-index: 1;
            height: 100%;
            width: 100%;
        }
        
        .video-thumbnail {
            width: 100%;
            height: 100%;
            object-fit: cover;
            border-radius: 12px;
            transition: all 0.3s ease;
        }
        
        .video-overlay {
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(to bottom, transparent 0%, rgba(0,0,0,0.7) 100%);
            display: flex;
            flex-direction: column;
            justify-content: flex-end;
            padding: 10px;
            border-radius: 12px;
            opacity: 0;
            transition: all 0.3s ease;
        }
        
        .video-item:hover .video-overlay {
            opacity: 1;
        }
        
        .video-item:hover .video-thumbnail {
            transform: scale(1.05);
        }
        
        .video-play-icon {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(102, 126, 234, 0.9);
            border-radius: 50%;
            width: 60px;
            height: 60px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            color: white;
            opacity: 0;
            transition: all 0.3s ease;
        }
        
        .video-item:hover .video-play-icon {
            opacity: 1;
            transform: translate(-50%, -50%) scale(1.1);
        }
        
        .video-name {
            font-size: 0.8rem;
            font-weight: 500;
            color: #ffffff;
            word-break: break-word;
            margin-bottom: 3px;
            line-height: 1.2;
        }
        
        .video-duration {
            font-size: 0.7rem;
            color: #a0a0a0;
            background: rgba(0, 0, 0, 0.7);
            padding: 2px 6px;
            border-radius: 8px;
            display: inline-block;
        }
        
        .video-fallback {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100%;
            padding: 15px;
        }
        
        .video-fallback i {
            font-size: 2rem;
            color: #667eea;
            margin-bottom: 10px;
        }
        
        .video-fallback .video-name {
            font-size: 0.8rem;
            font-weight: 500;
            color: #ffffff;
            word-break: break-word;
            text-align: center;
            line-height: 1.2;
        }
        
        .no-videos {
            text-align: center;
            padding: 40px;
            color: #a0a0a0;
            font-style: italic;
        }
        
        .no-videos i {
            font-size: 3rem;
            color: #667eea;
            margin-bottom: 20px;
            display: block;
        }
        
        .loading {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid rgba(255, 255, 255, 0.3);
            border-radius: 50%;
            border-top-color: #667eea;
            animation: spin 1s ease-in-out infinite;
        }
        
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        
        .stats {
            display: flex;
            justify-content: center;
            gap: 30px;
            margin: 30px 0;
            flex-wrap: wrap;
        }
        
        .stat-item {
            text-align: center;
            padding: 20px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 15px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            min-width: 120px;
        }
        
        .stat-number {
            font-size: 2rem;
            font-weight: 700;
            color: #667eea;
            display: block;
        }
        
        .stat-label {
            font-size: 0.9rem;
            color: #a0a0a0;
            margin-top: 5px;
        }
        
        @media (max-width: 768px) {
            .container {
                padding: 15px;
            }
            
            .header h1 {
                font-size: 2.5rem;
            }
            
            .video-list {
                grid-template-columns: 1fr;
            }
            
            .info-grid {
                grid-template-columns: 1fr;
            }
            
            .stats {
                gap: 15px;
            }
        }
        
        .fade-in {
            animation: fadeIn 0.6s ease-in-out;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .regenerate-btn {
            background: rgba(102, 126, 234, 0.8);
            border: none;
            border-radius: 10px;
            padding: 12px 25px;
            color: white;
            cursor: pointer;
            transition: all 0.3s ease;
            font-size: 1rem;
            font-weight: 500;
            display: inline-flex;
            align-items: center;
            gap: 10px;
        }
        
        .regenerate-btn:hover {
            background: rgba(102, 126, 234, 1);
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
        }
        
        .regenerate-btn:disabled {
            background: rgba(255, 255, 255, 0.2);
            cursor: not-allowed;
            transform: none;
        }
        
        .regenerate-btn i {
            transition: transform 0.3s ease;
        }
        
        .regenerate-btn.loading i {
            animation: spin 1s linear infinite;
        }
    </style>
</head>
<body>
    <div class="background-animation"></div>
    
    <div class="container">
        <div class="header fade-in">
            <h1><i class="fas fa-video"></i> {{ app_title }}</h1>
            <p class="subtitle">Servidor de Streaming Local</p>
        </div>
        
        <div class="server-info fade-in">
            <h3><i class="fas fa-server"></i> Información del Servidor</h3>
            <div class="info-grid">
                <div class="info-item">
                    <i class="fas fa-network-wired"></i>
                    <span><strong>IP Local:</strong> {{ ip_local }}</span>
                </div>
                <div class="info-item">
                    <i class="fas fa-plug"></i>
                    <span><strong>Puerto:</strong> 5000</span>
                </div>
                <div class="info-item">
                    <i class="fas fa-tv"></i>
                    <span><strong>TV:</strong> http://{{ ip_local }}:5000</span>
                </div>
                <div class="info-item">
                    <i class="fas fa-desktop"></i>
                    <span><strong>Local:</strong> http://localhost:5000</span>
                </div>
            </div>
            <div style="margin-top: 20px; text-align: center; display: flex; gap: 15px; justify-content: center; flex-wrap: wrap;">
                <button class="regenerate-btn" onclick="regenerateThumbnails()" id="regenerateBtn">
                    <i class="fas fa-sync-alt"></i> Regenerar Miniaturas
                </button>
                <button class="regenerate-btn" onclick="refreshProgress()" id="refreshProgressBtn" style="background: rgba(46, 204, 113, 0.8);">
                    <i class="fas fa-chart-line"></i> Actualizar Progreso
                </button>
            </div>
        </div>

        {% set archivos_principales = obtener_archivos_video() %}
        {% set carpetas = obtener_carpetas() %}
        
        <div class="stats fade-in">
            <div class="stat-item">
                <span class="stat-number">{{ archivos_principales|length }}</span>
                <div class="stat-label">Archivos</div>
            </div>
            <div class="stat-item">
                <span class="stat-number">{{ carpetas|length }}</span>
                <div class="stat-label">Carpetas</div>
            </div>
        </div>
        
        {% if archivos_principales %}
            <div class="capitulo fade-in">
                <h2><i class="fas fa-folder-open"></i>Capítulos Disponibles</h2>
                <div class="video-list">
                {% for archivo in archivos_principales %}
                    <div class="video-item" data-video="{{ archivo }}">
                        <a href="/player/{{ archivo }}" target="_blank">
                            <div class="video-fallback">
                                <i class="fas fa-video"></i>
                                <div class="video-name">{{ archivo }}</div>
                            </div>
                            <div class="video-play-icon">
                                <i class="fas fa-play"></i>
                            </div>
                            <div class="video-overlay">
                                <div class="video-name">{{ archivo }}</div>
                                <div class="video-duration" id="duration-{{ loop.index }}">Cargando...</div>
                            </div>
                            <div class="progress-bar" id="progress-{{ loop.index }}" style="width: 0%"></div>
                            <div class="video-status" id="status-{{ loop.index }}" style="display: none;"></div>
                        </a>
                    </div>
                {% endfor %}
                </div>
            </div>
        {% endif %}

        {% if carpetas %}
            {% for carpeta in carpetas %}
                <div class="capitulo fade-in">
                    <h2><i class="fas fa-folder"></i> {{ carpeta.upper() }}</h2>
                    {% set archivos = obtener_archivos_video_carpeta(carpeta) %}
                    {% if archivos %}
                        <div class="video-list">
                            {% for archivo in archivos %}
                                <div class="video-item" data-video="{{ carpeta }}/{{ archivo }}">
                                    <a href="/player/{{ carpeta }}/{{ archivo }}" target="_blank">
                                        <div class="video-fallback">
                                            <i class="fas fa-video"></i>
                                            <div class="video-name">{{ archivo }}</div>
                                        </div>
                                        <div class="video-play-icon">
                                            <i class="fas fa-play"></i>
                                        </div>
                                        <div class="video-overlay">
                                            <div class="video-name">{{ archivo }}</div>
                                            <div class="video-duration" id="duration-{{ loop.index }}">Cargando...</div>
                                        </div>
                                        <div class="progress-bar" id="progress-{{ loop.index }}" style="width: 0%"></div>
                                        <div class="video-status" id="status-{{ loop.index }}" style="display: none;"></div>
                                    </a>
                                </div>
                            {% endfor %}
                        </div>
                    {% else %}
                        <div class="no-videos">
                            <i class="fas fa-folder-open"></i>
                            <p>No se encontraron archivos de video en esta carpeta</p>
                        </div>
                    {% endif %}
                </div>
            {% endfor %}
        {% endif %}

        {% if not archivos_principales and not carpetas %}
            <div class="no-videos fade-in">
                <i class="fas fa-exclamation-triangle"></i>
                <h2>No se encontraron archivos de video</h2>
                <p>Verifica que la ruta <code>{{ ruta_capitulos }}</code> exista y contenga archivos de video.</p>
            </div>
        {% endif %}
    </div>
    
    <script>
        // Agregar efecto de carga suave
        document.addEventListener('DOMContentLoaded', function() {
            const items = document.querySelectorAll('.fade-in');
            items.forEach((item, index) => {
                setTimeout(() => {
                    item.style.opacity = '1';
                    item.style.transform = 'translateY(0)';
                }, index * 100);
            });
            
            // Cargar miniaturas de video y progreso
            loadVideoThumbnails();
            loadViewingProgress();
            
            // Actualizar progreso cada 30 segundos
            setInterval(loadViewingProgress, 30000);
        });
        
        async function loadVideoThumbnails() {
            const videoItems = document.querySelectorAll('.video-item[data-video]');
            
            for (let i = 0; i < videoItems.length; i++) {
                const item = videoItems[i];
                const videoPath = item.getAttribute('data-video');
                const durationElement = item.querySelector('.video-duration');
                const fallbackElement = item.querySelector('.video-fallback');
                
                try {
                    const response = await fetch(`/api/thumbnail/${encodeURIComponent(videoPath)}`);
                    const data = await response.json();
                    
                    if (data.thumbnail) {
                        // Crear elemento de imagen para la miniatura
                        const img = document.createElement('img');
                        img.src = data.thumbnail;
                        img.className = 'video-thumbnail';
                        img.alt = videoPath;
                        
                        // Reemplazar el fallback con la miniatura
                        fallbackElement.style.display = 'none';
                        item.querySelector('a').insertBefore(img, fallbackElement);
                        
                        // Mostrar duración
                        if (durationElement && data.duration) {
                            durationElement.textContent = data.duration;
                        }
                    } else {
                        // Si no hay miniatura, mostrar duración en el fallback
                        if (durationElement && data.duration) {
                            durationElement.textContent = data.duration;
                        }
                    }
                } catch (error) {
                    console.log('Error cargando miniatura para:', videoPath);
                    if (durationElement) {
                        durationElement.textContent = 'Error';
                    }
                }
                
                // Pequeña pausa para no sobrecargar el servidor
                await new Promise(resolve => setTimeout(resolve, 100));
            }
        }
        
        async function regenerateThumbnails() {
            const btn = document.getElementById('regenerateBtn');
            const icon = btn.querySelector('i');
            const originalText = btn.innerHTML;
            
            // Mostrar estado de carga
            btn.disabled = true;
            btn.classList.add('loading');
            btn.innerHTML = '<i class="fas fa-sync-alt"></i> Regenerando...';
            
            try {
                const response = await fetch('/api/regenerate-thumbnails');
                const data = await response.json();
                
                if (data.success) {
                    btn.innerHTML = '<i class="fas fa-check"></i> ¡Completado!';
                    btn.style.background = 'rgba(76, 175, 80, 0.8)';
                    
                    // Recargar miniaturas después de 2 segundos
                    setTimeout(() => {
                        location.reload();
                    }, 2000);
                } else {
                    btn.innerHTML = '<i class="fas fa-exclamation-triangle"></i> Error';
                    btn.style.background = 'rgba(244, 67, 54, 0.8)';
                    
                    setTimeout(() => {
                        btn.innerHTML = originalText;
                        btn.style.background = '';
                        btn.disabled = false;
                        btn.classList.remove('loading');
                    }, 3000);
                }
            } catch (error) {
                console.error('Error regenerando miniaturas:', error);
                btn.innerHTML = '<i class="fas fa-exclamation-triangle"></i> Error';
                btn.style.background = 'rgba(244, 67, 54, 0.8)';
                
                setTimeout(() => {
                    btn.innerHTML = originalText;
                    btn.style.background = '';
                    btn.disabled = false;
                    btn.classList.remove('loading');
                }, 3000);
            }
        }
        
        async function loadViewingProgress() {
            try {
                console.log('Cargando progreso de visualización...');
                const response = await fetch('/api/progress/all');
                const data = await response.json();
                
                console.log('Datos de progreso recibidos:', data);
                
                if (data.success) {
                    const progressData = data.progress;
                    const videoItems = document.querySelectorAll('.video-item[data-video]');
                    
                    console.log(`Procesando ${videoItems.length} videos...`);
                    
                    videoItems.forEach((item, index) => {
                        const videoPath = item.getAttribute('data-video');
                        const progress = progressData[videoPath];
                        
                        console.log(`Video: ${videoPath}, Progreso:`, progress);
                        
                        const progressBar = item.querySelector('.progress-bar');
                        const statusElement = item.querySelector('.video-status');
                        
                        if (progress && progress.progress_percentage > 0) {
                            if (progressBar) {
                                progressBar.style.width = progress.progress_percentage + '%';
                                progressBar.style.display = 'block';
                                
                                if (progress.is_completed) {
                                    progressBar.classList.add('completed');
                                } else {
                                    progressBar.classList.remove('completed');
                                }
                                
                                console.log(`Barra de progreso actualizada: ${progress.progress_percentage}%`);
                            }
                            
                            if (statusElement) {
                                statusElement.style.display = 'block';
                                
                                if (progress.is_completed) {
                                    statusElement.textContent = '✓ Completado';
                                    statusElement.className = 'video-status completed';
                                } else {
                                    statusElement.textContent = '▶ En progreso';
                                    statusElement.className = 'video-status in-progress';
                                }
                            }
                        } else {
                            // No hay progreso, ocultar elementos
                            if (progressBar) {
                                progressBar.style.width = '0%';
                                progressBar.style.display = 'none';
                            }
                            if (statusElement) {
                                statusElement.style.display = 'none';
                            }
                        }
                    });
                }
            } catch (error) {
                console.log('Error cargando progreso de visualización:', error);
            }
        }
        
        function refreshProgress() {
            const btn = document.getElementById('refreshProgressBtn');
            const icon = btn.querySelector('i');
            const originalText = btn.innerHTML;
            
            // Mostrar estado de carga
            btn.disabled = true;
            btn.classList.add('loading');
            btn.innerHTML = '<i class="fas fa-chart-line"></i> Actualizando...';
            
            // Recargar progreso
            loadViewingProgress().then(() => {
                btn.innerHTML = '<i class="fas fa-check"></i> ¡Actualizado!';
                btn.style.background = 'rgba(46, 204, 113, 1)';
                
                setTimeout(() => {
                    btn.innerHTML = originalText;
                    btn.style.background = 'rgba(46, 204, 113, 0.8)';
                    btn.disabled = false;
                    btn.classList.remove('loading');
                }, 2000);
            }).catch((error) => {
                console.error('Error actualizando progreso:', error);
                btn.innerHTML = '<i class="fas fa-exclamation-triangle"></i> Error';
                btn.style.background = 'rgba(244, 67, 54, 0.8)';
                
                setTimeout(() => {
                    btn.innerHTML = originalText;
                    btn.style.background = 'rgba(46, 204, 113, 0.8)';
                    btn.disabled = false;
                    btn.classList.remove('loading');
                }, 3000);
            });
        }
    </script>
</body>
</html>
"""
