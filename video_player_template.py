"""
Template para el reproductor de video en pantalla completa
"""

VIDEO_PLAYER_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ video_name }} - {{ app_title }}</title>
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
            background: #000;
            color: #fff;
            overflow: hidden;
            height: 100vh;
        }
        
        .video-container {
            position: relative;
            width: 100vw;
            height: 100vh;
            background: #000;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .video-player {
            width: 100%;
            height: 100%;
            object-fit: contain;
            outline: none;
            cursor: pointer;
        }
        
        .video-player:hover {
            cursor: pointer;
        }
        
        .click-overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: transparent;
            cursor: pointer;
            z-index: 5;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .click-indicator {
            background: rgba(0, 0, 0, 0.7);
            border-radius: 50%;
            width: 80px;
            height: 80px;
            display: flex;
            align-items: center;
            justify-content: center;
            opacity: 0;
            transition: opacity 0.3s ease;
            pointer-events: none;
        }
        
        .click-indicator.show {
            opacity: 1;
        }
        
        .click-indicator i {
            font-size: 2rem;
            color: white;
        }
        
        .tv-help {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.9);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 1000;
            opacity: 0;
            visibility: hidden;
            transition: all 0.3s ease;
        }
        
        .tv-help.show {
            opacity: 1;
            visibility: visible;
        }
        
        .help-content {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(20px);
            border-radius: 20px;
            padding: 30px;
            max-width: 500px;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .help-content h3 {
            color: white;
            margin-bottom: 20px;
            font-size: 1.5rem;
        }
        
        .help-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin-bottom: 20px;
        }
        
        .help-item {
            background: rgba(255, 255, 255, 0.1);
            padding: 10px;
            border-radius: 8px;
            color: white;
            font-size: 0.9rem;
        }
        
        .help-item kbd {
            background: rgba(255, 255, 255, 0.2);
            padding: 2px 6px;
            border-radius: 4px;
            font-family: monospace;
            font-size: 0.8rem;
        }
        
        .help-close {
            background: rgba(102, 126, 234, 0.8);
            border: none;
            border-radius: 8px;
            padding: 10px 20px;
            color: white;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .help-close:hover {
            background: rgba(102, 126, 234, 1);
        }
        
        .video-controls {
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            background: linear-gradient(transparent, rgba(0, 0, 0, 0.8));
            padding: 20px;
            transform: translateY(100%);
            transition: transform 0.3s ease;
            z-index: 10;
        }
        
        .video-container:hover .video-controls {
            transform: translateY(0);
        }
        
        .controls-row {
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 10px;
        }
        
        .play-pause-btn {
            background: rgba(102, 126, 234, 0.9);
            border: none;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            color: white;
            font-size: 1.2rem;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .play-pause-btn:hover {
            background: rgba(102, 126, 234, 1);
            transform: scale(1.1);
        }
        
        .progress-container {
            flex: 1;
            height: 6px;
            background: rgba(255, 255, 255, 0.3);
            border-radius: 3px;
            cursor: pointer;
            position: relative;
            transition: height 0.2s ease;
        }
        
        .progress-container:hover {
            height: 8px;
        }
        
        .progress-preview {
            position: absolute;
            bottom: 15px;
            background: rgba(0, 0, 0, 0.8);
            color: white;
            padding: 5px 10px;
            border-radius: 4px;
            font-size: 0.8rem;
            pointer-events: none;
            opacity: 0;
            transition: opacity 0.2s ease;
            z-index: 1000;
        }
        
        .progress-preview.show {
            opacity: 1;
        }
        
        .progress-bar {
            height: 100%;
            background: #667eea;
            border-radius: 3px;
            width: 0%;
            transition: width 0.1s ease;
        }
        
        .time-display {
            color: #fff;
            font-size: 0.9rem;
            min-width: 100px;
            text-align: center;
        }
        
        .volume-container {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .volume-slider {
            width: 80px;
            height: 4px;
            background: rgba(255, 255, 255, 0.3);
            border-radius: 2px;
            outline: none;
            cursor: pointer;
        }
        
        .volume-slider::-webkit-slider-thumb {
            appearance: none;
            width: 16px;
            height: 16px;
            background: #667eea;
            border-radius: 50%;
            cursor: pointer;
        }
        
        .fullscreen-btn, .back-btn {
            background: rgba(255, 255, 255, 0.2);
            border: none;
            border-radius: 8px;
            padding: 10px 15px;
            color: white;
            cursor: pointer;
            transition: all 0.3s ease;
            font-size: 0.9rem;
        }
        
        .fullscreen-btn:hover, .back-btn:hover {
            background: rgba(255, 255, 255, 0.3);
            transform: translateY(-2px);
        }
        
        .video-title {
            position: absolute;
            top: 20px;
            left: 20px;
            background: rgba(0, 0, 0, 0.7);
            padding: 10px 20px;
            border-radius: 10px;
            font-size: 1.1rem;
            font-weight: 500;
            opacity: 0;
            transition: opacity 0.3s ease;
        }
        
        .video-container:hover .video-title {
            opacity: 1;
        }
        
        .loading-spinner {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 60px;
            height: 60px;
            border: 4px solid rgba(255, 255, 255, 0.3);
            border-top: 4px solid #667eea;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            z-index: 5;
        }
        
        @keyframes spin {
            0% { transform: translate(-50%, -50%) rotate(0deg); }
            100% { transform: translate(-50%, -50%) rotate(360deg); }
        }
        
        .error-message {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            text-align: center;
            background: rgba(0, 0, 0, 0.8);
            padding: 30px;
            border-radius: 15px;
            border: 2px solid #ff6b6b;
        }
        
        .error-message i {
            font-size: 3rem;
            color: #ff6b6b;
            margin-bottom: 15px;
        }
        
        .next-episode-countdown {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(0, 0, 0, 0.9);
            padding: 40px;
            border-radius: 20px;
            text-align: center;
            border: 2px solid #667eea;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
            opacity: 0;
            transition: all 0.3s ease;
            z-index: 20;
        }
        
        .next-episode-countdown.show {
            opacity: 1;
        }
        
        .countdown-title {
            font-size: 1.5rem;
            font-weight: 600;
            color: #ffffff;
            margin-bottom: 20px;
        }
        
        .next-episode-info {
            font-size: 1.1rem;
            color: #a0a0a0;
            margin-bottom: 25px;
        }
        
        .countdown-timer {
            font-size: 4rem;
            font-weight: 700;
            color: #667eea;
            margin-bottom: 20px;
            text-shadow: 0 0 20px rgba(102, 126, 234, 0.5);
        }
        
        .countdown-controls {
            display: flex;
            gap: 15px;
            justify-content: center;
        }
        
        .countdown-btn {
            background: rgba(102, 126, 234, 0.8);
            border: none;
            border-radius: 10px;
            padding: 12px 25px;
            color: white;
            cursor: pointer;
            transition: all 0.3s ease;
            font-size: 1rem;
            font-weight: 500;
        }
        
        .countdown-btn:hover {
            background: rgba(102, 126, 234, 1);
            transform: translateY(-2px);
        }
        
        .countdown-btn.secondary {
            background: rgba(255, 255, 255, 0.2);
        }
        
        .countdown-btn.secondary:hover {
            background: rgba(255, 255, 255, 0.3);
        }
        
        .auto-advance-notification {
            position: absolute;
            top: 20px;
            right: 20px;
            background: rgba(0, 0, 0, 0.9);
            padding: 15px 20px;
            border-radius: 15px;
            border: 2px solid #667eea;
            box-shadow: 0 5px 20px rgba(0, 0, 0, 0.5);
            opacity: 0;
            transform: translateX(100%);
            transition: all 0.3s ease;
            z-index: 15;
            max-width: 300px;
        }
        
        .auto-advance-notification.show {
            opacity: 1;
            transform: translateX(0);
        }
        
        .auto-advance-title {
            font-size: 1rem;
            font-weight: 600;
            color: #667eea;
            margin-bottom: 8px;
        }
        
        .auto-advance-info {
            font-size: 0.9rem;
            color: #ffffff;
            margin-bottom: 10px;
        }
        
        .auto-advance-timer {
            font-size: 1.2rem;
            font-weight: 700;
            color: #667eea;
            text-align: center;
            margin-bottom: 10px;
        }
        
        .auto-advance-controls {
            display: flex;
            gap: 10px;
            justify-content: center;
        }
        
        .auto-advance-btn {
            background: rgba(102, 126, 234, 0.8);
            border: none;
            border-radius: 8px;
            padding: 8px 15px;
            color: white;
            cursor: pointer;
            transition: all 0.3s ease;
            font-size: 0.8rem;
            font-weight: 500;
        }
        
        .auto-advance-btn:hover {
            background: rgba(102, 126, 234, 1);
            transform: translateY(-1px);
        }
        
        .auto-advance-btn.secondary {
            background: rgba(255, 255, 255, 0.2);
        }
        
        .auto-advance-btn.secondary:hover {
            background: rgba(255, 255, 255, 0.3);
        }
        
        .navigation-buttons {
            position: absolute;
            top: 50%;
            transform: translateY(-50%);
            display: flex;
            justify-content: space-between;
            width: 100%;
            padding: 0 20px;
            opacity: 0;
            transition: opacity 0.3s ease;
        }
        
        .video-container:hover .navigation-buttons {
            opacity: 1;
        }
        
        .nav-btn {
            background: rgba(0, 0, 0, 0.7);
            border: none;
            border-radius: 50%;
            width: 60px;
            height: 60px;
            color: white;
            font-size: 1.5rem;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .nav-btn:hover {
            background: rgba(102, 126, 234, 0.9);
            transform: scale(1.1);
        }
        
        .nav-btn:disabled {
            opacity: 0.3;
            cursor: not-allowed;
        }
        
        @media (max-width: 768px) {
            .video-controls {
                padding: 15px;
            }
            
            .controls-row {
                gap: 10px;
            }
            
            .play-pause-btn {
                width: 45px;
                height: 45px;
                font-size: 1rem;
            }
            
            .volume-container {
                display: none;
            }
            
            .time-display {
                min-width: 80px;
                font-size: 0.8rem;
            }
        }
    </style>
</head>
<body>
    <div class="video-container" id="videoContainer">
        <div class="loading-spinner" id="loadingSpinner"></div>
        
        <div class="video-title" id="videoTitle">{{ video_name }}</div>
        
        <div class="navigation-buttons">
            <button class="nav-btn" id="prevBtn" onclick="navigateVideo(-1)" title="Video anterior">
                <i class="fas fa-chevron-left"></i>
            </button>
            <button class="nav-btn" id="nextBtn" onclick="navigateVideo(1)" title="Siguiente video">
                <i class="fas fa-chevron-right"></i>
            </button>
        </div>
        
        <video 
            id="videoPlayer" 
            class="video-player" 
            preload="metadata"
            onloadeddata="onVideoLoaded()"
            onerror="onVideoError()"
            onended="onVideoEnded()"
            onclick="togglePlayPause()"
        >
            <source src="{{ video_url }}" type="video/mp4">
            Tu navegador no soporta el elemento de video.
        </video>
        
        <!-- Overlay de click para TV -->
        <div class="click-overlay" id="clickOverlay" onclick="togglePlayPause()">
            <div class="click-indicator" id="clickIndicator">
                <i class="fas fa-play" id="clickPlayIcon"></i>
                <i class="fas fa-pause" id="clickPauseIcon" style="display: none;"></i>
            </div>
        </div>
        
        <div class="video-controls">
            <div class="controls-row">
                <button class="play-pause-btn" id="playPauseBtn" onclick="togglePlayPause()">
                    <i class="fas fa-play"></i>
                </button>
                
                <div class="progress-container" onclick="seekVideo(event)" onmousemove="showProgressPreview(event)" onmouseleave="hideProgressPreview()">
                    <div class="progress-bar" id="progressBar"></div>
                    <div class="progress-preview" id="progressPreview"></div>
                </div>
                
                <div class="time-display" id="timeDisplay">00:00 / 00:00</div>
                
                <div class="volume-container">
                    <i class="fas fa-volume-up" id="volumeIcon"></i>
                    <input type="range" class="volume-slider" id="volumeSlider" min="0" max="1" step="0.1" value="1" onchange="setVolume(this.value)">
                </div>
                
                <button class="fullscreen-btn" onclick="toggleFullscreen()" title="Pantalla completa">
                    <i class="fas fa-expand"></i>
                </button>
                
                <button class="fullscreen-btn" id="autoAdvanceToggle" onclick="toggleAutoAdvance()" title="Auto-avance">
                    <i class="fas fa-forward"></i>
                </button>
                
                <button class="fullscreen-btn" onclick="showTvHelp()" title="Ayuda de controles">
                    <i class="fas fa-question-circle"></i>
                </button>
                
                <button class="back-btn" onclick="goBack()" title="Volver al menú">
                    <i class="fas fa-arrow-left"></i> Volver
                </button>
            </div>
        </div>
        
        <div class="error-message" id="errorMessage" style="display: none;">
            <i class="fas fa-exclamation-triangle"></i>
            <h3>Error al cargar el video</h3>
            <p>No se pudo reproducir el archivo de video.</p>
            <button class="back-btn" onclick="goBack()" style="margin-top: 15px;">
                <i class="fas fa-arrow-left"></i> Volver al menú
            </button>
        </div>
        
        <!-- Ayuda de controles para TV -->
        <div class="tv-help" id="tvHelp">
            <div class="help-content">
                <h3><i class="fas fa-tv"></i> Controles para TV</h3>
                <div class="help-grid">
                    <div class="help-item">
                        <kbd>Click</kbd> o <kbd>Espacio</kbd> - Pausar/Reproducir
                    </div>
                    <div class="help-item">
                        <kbd>←</kbd> <kbd>→</kbd> - Video anterior/siguiente
                    </div>
                    <div class="help-item">
                        <kbd>F</kbd> - Pantalla completa
                    </div>
                    <div class="help-item">
                        <kbd>Esc</kbd> - Salir de pantalla completa
                    </div>
                </div>
                <button class="help-close" onclick="hideTvHelp()">
                    <i class="fas fa-times"></i> Cerrar
                </button>
            </div>
        </div>
        
        <div class="next-episode-countdown" id="nextEpisodeCountdown">
            <div class="countdown-title">Siguiente Capítulo</div>
            <div class="next-episode-info" id="nextEpisodeInfo">El siguiente capítulo comenzará en</div>
            <div class="countdown-timer" id="countdownTimer">5</div>
            <div class="countdown-controls">
                <button class="countdown-btn secondary" onclick="cancelCountdown()">
                    <i class="fas fa-times"></i> Cancelar
                </button>
                <button class="countdown-btn" onclick="playNextEpisode()">
                    <i class="fas fa-play"></i> Reproducir Ahora
                </button>
            </div>
        </div>
        
        <div class="auto-advance-notification" id="autoAdvanceNotification">
            <div class="auto-advance-title">Auto-avance</div>
            <div class="auto-advance-info" id="autoAdvanceInfo">El siguiente capítulo comenzará automáticamente en</div>
            <div class="auto-advance-timer" id="autoAdvanceTimer">{{ auto_advance_countdown_seconds }}</div>
            <div class="auto-advance-controls">
                <button class="auto-advance-btn secondary" onclick="cancelAutoAdvance()">
                    <i class="fas fa-times"></i> Cancelar
                </button>
                <button class="auto-advance-btn" onclick="advanceNow()">
                    <i class="fas fa-forward"></i> Ahora
                </button>
            </div>
        </div>
    </div>
    
    <script>
        const video = document.getElementById('videoPlayer');
        const playPauseBtn = document.getElementById('playPauseBtn');
        const progressBar = document.getElementById('progressBar');
        const timeDisplay = document.getElementById('timeDisplay');
        const volumeSlider = document.getElementById('volumeSlider');
        const volumeIcon = document.getElementById('volumeIcon');
        const loadingSpinner = document.getElementById('loadingSpinner');
        const errorMessage = document.getElementById('errorMessage');
        const videoContainer = document.getElementById('videoContainer');
        const videoTitle = document.getElementById('videoTitle');
        const nextEpisodeCountdown = document.getElementById('nextEpisodeCountdown');
        const nextEpisodeInfo = document.getElementById('nextEpisodeInfo');
        const countdownTimer = document.getElementById('countdownTimer');
        const autoAdvanceNotification = document.getElementById('autoAdvanceNotification');
        const autoAdvanceInfo = document.getElementById('autoAdvanceInfo');
        const autoAdvanceTimer = document.getElementById('autoAdvanceTimer');
        
        let isPlaying = false;
        let isFullscreen = false;
        let countdownInterval = null;
        let countdownSeconds = 5;
        let autoAdvanceInterval = null;
        let autoAdvanceSeconds = {{ auto_advance_countdown_seconds }};
        let autoAdvanceEnabled = true; // Configuración de auto-avance
        let progressSaveInterval = null;
        let lastSavedTime = 0;
        
        // Datos del video actual
        const currentVideo = {
            name: '{{ video_name }}',
            url: '{{ video_url }}',
            index: {{ video_index }},
            total: {{ total_videos }}
        };
        
        // Lista de videos disponibles
        const videoList = {{ video_list | safe }};
        
        function onVideoLoaded() {
            loadingSpinner.style.display = 'none';
            video.volume = 1;
            
            // Cargar progreso existente
            loadExistingProgress();
            
            // Auto-play y pantalla completa
            setTimeout(() => {
                video.play().then(() => {
                    isPlaying = true;
                    updatePlayPauseButton();
                    enterFullscreen();
                }).catch(error => {
                    console.log('Auto-play falló:', error);
                    // Si auto-play falla, al menos entrar en pantalla completa
                    enterFullscreen();
                });
            }, 500);
        }
        
        async function loadExistingProgress() {
            try {
                const response = await fetch(`/api/progress/${encodeURIComponent(currentVideo.name)}`);
                const data = await response.json();
                
                if (data.success && data.progress) {
                    const progress = data.progress;
                    
                    // Si el video no está completado y tiene progreso, saltar a esa posición
                    if (!progress.is_completed && progress.current_time > 0) {
                        video.currentTime = progress.current_time;
                        console.log(`Progreso cargado: ${progress.current_time}s (${progress.progress_percentage}%)`);
                    }
                }
            } catch (error) {
                console.log('Error cargando progreso existente:', error);
            }
        }
        
        function onVideoError() {
            loadingSpinner.style.display = 'none';
            errorMessage.style.display = 'block';
        }
        
        function onVideoEnded() {
            // Marcar video como completado
            markVideoCompleted();
            
            // Mostrar countdown para el siguiente video si existe
            if (currentVideo.index < currentVideo.total - 1) {
                showNextEpisodeCountdown();
            }
        }
        
        function togglePlayPause() {
            if (isPlaying) {
                video.pause();
                isPlaying = false;
                // Guardar progreso al pausar
                saveProgress();
            } else {
                video.play();
                isPlaying = true;
            }
            updatePlayPauseButton();
            showClickIndicator();
        }
        
        function showClickIndicator() {
            const clickIndicator = document.getElementById('clickIndicator');
            const clickPlayIcon = document.getElementById('clickPlayIcon');
            const clickPauseIcon = document.getElementById('clickPauseIcon');
            
            // Mostrar el indicador
            clickIndicator.classList.add('show');
            
            // Actualizar el icono según el estado
            if (isPlaying) {
                clickPlayIcon.style.display = 'none';
                clickPauseIcon.style.display = 'block';
            } else {
                clickPlayIcon.style.display = 'block';
                clickPauseIcon.style.display = 'none';
            }
            
            // Ocultar después de 1 segundo
            setTimeout(() => {
                clickIndicator.classList.remove('show');
            }, 1000);
        }
        
        function showTvHelp() {
            const tvHelp = document.getElementById('tvHelp');
            tvHelp.classList.add('show');
        }
        
        function hideTvHelp() {
            const tvHelp = document.getElementById('tvHelp');
            tvHelp.classList.remove('show');
        }
        
        function updatePlayPauseButton() {
            const icon = playPauseBtn.querySelector('i');
            if (isPlaying) {
                icon.className = 'fas fa-pause';
            } else {
                icon.className = 'fas fa-play';
            }
        }
        
        function seekVideo(event) {
            if (!video.duration) return;
            
            const progressContainer = event.currentTarget;
            const rect = progressContainer.getBoundingClientRect();
            const clickX = event.clientX - rect.left;
            const pos = Math.max(0, Math.min(1, clickX / rect.width));
            
            // Actualizar tiempo del video
            video.currentTime = pos * video.duration;
            
            // Actualizar barra de progreso inmediatamente
            updateProgress();
            
            // Guardar progreso
            saveProgress();
        }
        
        function showProgressPreview(event) {
            if (!video.duration) return;
            
            const progressContainer = event.currentTarget;
            const rect = progressContainer.getBoundingClientRect();
            const clickX = event.clientX - rect.left;
            const pos = Math.max(0, Math.min(1, clickX / rect.width));
            const time = pos * video.duration;
            
            const preview = document.getElementById('progressPreview');
            preview.textContent = formatTime(time) + ' / ' + formatTime(video.duration);
            preview.style.left = (clickX - 30) + 'px';
            preview.classList.add('show');
        }
        
        function hideProgressPreview() {
            const preview = document.getElementById('progressPreview');
            preview.classList.remove('show');
        }
        
        function formatTime(seconds) {
            const hours = Math.floor(seconds / 3600);
            const minutes = Math.floor((seconds % 3600) / 60);
            const secs = Math.floor(seconds % 60);
            
            if (hours > 0) {
                return `${hours}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
            } else {
                return `${minutes}:${secs.toString().padStart(2, '0')}`;
            }
        }
        
        function setVolume(value) {
            video.volume = value;
            const icon = volumeIcon;
            if (value == 0) {
                icon.className = 'fas fa-volume-mute';
            } else if (value < 0.5) {
                icon.className = 'fas fa-volume-down';
            } else {
                icon.className = 'fas fa-volume-up';
            }
        }
        
        function toggleFullscreen() {
            if (!isFullscreen) {
                enterFullscreen();
            } else {
                exitFullscreen();
            }
        }
        
        function enterFullscreen() {
            if (videoContainer.requestFullscreen) {
                videoContainer.requestFullscreen();
            } else if (videoContainer.webkitRequestFullscreen) {
                videoContainer.webkitRequestFullscreen();
            } else if (videoContainer.msRequestFullscreen) {
                videoContainer.msRequestFullscreen();
            }
            isFullscreen = true;
        }
        
        function exitFullscreen() {
            if (document.exitFullscreen) {
                document.exitFullscreen();
            } else if (document.webkitExitFullscreen) {
                document.webkitExitFullscreen();
            } else if (document.msExitFullscreen) {
                document.msExitFullscreen();
            }
            isFullscreen = false;
        }
        
        function navigateVideo(direction) {
            const newIndex = currentVideo.index + direction;
            if (newIndex >= 0 && newIndex < videoList.length) {
                const nextVideo = videoList[newIndex];
                window.location.href = `/player/${encodeURIComponent(nextVideo.path)}`;
            }
        }
        
        function showNextEpisodeCountdown() {
            const nextVideo = videoList[currentVideo.index + 1];
            if (nextVideo) {
                nextEpisodeInfo.textContent = `El siguiente capítulo "${nextVideo.name}" comenzará en`;
                countdownSeconds = 5;
                countdownTimer.textContent = countdownSeconds;
                nextEpisodeCountdown.classList.add('show');
                
                // Iniciar countdown
                countdownInterval = setInterval(() => {
                    countdownSeconds--;
                    countdownTimer.textContent = countdownSeconds;
                    
                    if (countdownSeconds <= 0) {
                        clearInterval(countdownInterval);
                        playNextEpisode();
                    }
                }, 1000);
            }
        }
        
        function cancelCountdown() {
            if (countdownInterval) {
                clearInterval(countdownInterval);
                countdownInterval = null;
            }
            nextEpisodeCountdown.classList.remove('show');
        }
        
        function playNextEpisode() {
            if (countdownInterval) {
                clearInterval(countdownInterval);
                countdownInterval = null;
            }
            nextEpisodeCountdown.classList.remove('show');
            navigateVideo(1);
        }
        
        function showAutoAdvanceNotification() {
            const nextVideo = videoList[currentVideo.index + 1];
            if (nextVideo && autoAdvanceEnabled) {
                // Cancelar cualquier countdown anterior
                if (autoAdvanceInterval) {
                    clearInterval(autoAdvanceInterval);
                    autoAdvanceInterval = null;
                }
                
                autoAdvanceInfo.textContent = `El siguiente capítulo "${nextVideo.name}" comenzará automáticamente en`;
                autoAdvanceSeconds = {{ auto_advance_countdown_seconds }};
                autoAdvanceTimer.textContent = autoAdvanceSeconds;
                autoAdvanceNotification.classList.add('show');
                
                console.log(`Auto-avance iniciado: ${autoAdvanceSeconds} segundos`);
                
                // Iniciar countdown de auto-avance
                autoAdvanceInterval = setInterval(() => {
                    autoAdvanceSeconds--;
                    autoAdvanceTimer.textContent = autoAdvanceSeconds;
                    console.log(`Countdown: ${autoAdvanceSeconds}`);
                    
                    if (autoAdvanceSeconds <= 0) {
                        clearInterval(autoAdvanceInterval);
                        autoAdvanceInterval = null;
                        console.log('Auto-avance ejecutándose...');
                        advanceNow();
                    }
                }, 1000);
            }
        }
        
        function cancelAutoAdvance() {
            if (autoAdvanceInterval) {
                clearInterval(autoAdvanceInterval);
                autoAdvanceInterval = null;
            }
            autoAdvanceNotification.classList.remove('show');
            console.log('Auto-avance cancelado');
        }
        
        function advanceNow() {
            if (autoAdvanceInterval) {
                clearInterval(autoAdvanceInterval);
                autoAdvanceInterval = null;
            }
            autoAdvanceNotification.classList.remove('show');
            navigateVideo(1);
        }
        
        function toggleAutoAdvance() {
            autoAdvanceEnabled = !autoAdvanceEnabled;
            const toggleBtn = document.getElementById('autoAdvanceToggle');
            const icon = toggleBtn.querySelector('i');
            
            if (autoAdvanceEnabled) {
                icon.className = 'fas fa-forward';
                toggleBtn.title = 'Auto-avance: Activado';
                toggleBtn.style.background = 'rgba(102, 126, 234, 0.8)';
            } else {
                icon.className = 'fas fa-pause';
                toggleBtn.title = 'Auto-avance: Desactivado';
                toggleBtn.style.background = 'rgba(255, 255, 255, 0.2)';
                // Cancelar auto-avance si está activo
                cancelAutoAdvance();
            }
        }
        
        function goBack() {
            window.close();
            // Si no se puede cerrar la ventana, redirigir al menú principal
            setTimeout(() => {
                window.location.href = '/';
            }, 100);
        }
        
        function formatTime(seconds) {
            const hours = Math.floor(seconds / 3600);
            const minutes = Math.floor((seconds % 3600) / 60);
            const secs = Math.floor(seconds % 60);
            
            if (hours > 0) {
                return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
            } else {
                return `${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
            }
        }
        
        function updateProgress() {
            if (video.duration) {
                const progress = (video.currentTime / video.duration) * 100;
                progressBar.style.width = progress + '%';
                timeDisplay.textContent = `${formatTime(video.currentTime)} / ${formatTime(video.duration)}`;
                
                // Guardar progreso cada 10 segundos
                if (Math.floor(video.currentTime) % 10 === 0 && Math.floor(video.currentTime) !== lastSavedTime) {
                    saveProgress();
                    lastSavedTime = Math.floor(video.currentTime);
                }
                
                // Verificar si quedan {{ auto_advance_trigger_seconds }} segundos para el auto-avance
                const remainingTime = video.duration - video.currentTime;
                if (remainingTime <= {{ auto_advance_trigger_seconds }} && remainingTime > {{ auto_advance_trigger_seconds - 1 }} && autoAdvanceEnabled && currentVideo.index < currentVideo.total - 1) {
                    showAutoAdvanceNotification();
                }
            }
        }
        
        async function saveProgress() {
            try {
                const response = await fetch('/api/progress', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        video_name: currentVideo.name,
                        current_time: video.currentTime,
                        duration: video.duration,
                        is_completed: false
                    })
                });
                
                const data = await response.json();
                if (data.success) {
                    console.log('Progreso guardado:', data.progress);
                }
            } catch (error) {
                console.log('Error guardando progreso:', error);
            }
        }
        
        async function markVideoCompleted() {
            try {
                const response = await fetch('/api/progress', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        video_name: currentVideo.name,
                        current_time: video.duration,
                        duration: video.duration,
                        is_completed: true
                    })
                });
                
                const data = await response.json();
                if (data.success) {
                    console.log('Video marcado como completado:', data.progress);
                }
            } catch (error) {
                console.log('Error marcando video como completado:', error);
            }
        }
        
        // Event listeners
        video.addEventListener('play', () => {
            isPlaying = true;
            updatePlayPauseButton();
        });
        
        video.addEventListener('pause', () => {
            isPlaying = false;
            updatePlayPauseButton();
        });
        
        video.addEventListener('timeupdate', updateProgress);
        
        // Event listeners para navegación con teclado (optimizado para TV)
        document.addEventListener('keydown', (e) => {
            switch(e.key) {
                case ' ':
                case 'Enter':
                    e.preventDefault();
                    togglePlayPause();
                    break;
                case 'ArrowLeft':
                    e.preventDefault();
                    if (currentVideo.index > 0) {
                        navigateVideo(-1);
                    }
                    break;
                case 'ArrowRight':
                    e.preventDefault();
                    if (currentVideo.index < currentVideo.total - 1) {
                        navigateVideo(1);
                    }
                    break;
                case 'f':
                case 'F':
                    e.preventDefault();
                    toggleFullscreen();
                    break;
                case 'Escape':
                    e.preventDefault();
                    if (isFullscreen) {
                        exitFullscreen();
                    } else {
                        hideTvHelp();
                    }
                    break;
                case 'h':
                case 'H':
                case '?':
                    e.preventDefault();
                    showTvHelp();
                    break;
            }
        });
        
        video.addEventListener('loadedmetadata', () => {
            updateProgress();
        });
        
        // Controles de teclado
        document.addEventListener('keydown', (event) => {
            switch(event.code) {
                case 'Space':
                    event.preventDefault();
                    togglePlayPause();
                    break;
                case 'ArrowLeft':
                    event.preventDefault();
                    video.currentTime = Math.max(0, video.currentTime - 10);
                    break;
                case 'ArrowRight':
                    event.preventDefault();
                    video.currentTime = Math.min(video.duration, video.currentTime + 10);
                    break;
                case 'ArrowUp':
                    event.preventDefault();
                    video.volume = Math.min(1, video.volume + 0.1);
                    volumeSlider.value = video.volume;
                    setVolume(video.volume);
                    break;
                case 'ArrowDown':
                    event.preventDefault();
                    video.volume = Math.max(0, video.volume - 0.1);
                    volumeSlider.value = video.volume;
                    setVolume(video.volume);
                    break;
                case 'KeyF':
                    event.preventDefault();
                    toggleFullscreen();
                    break;
                case 'Escape':
                    if (isFullscreen) {
                        exitFullscreen();
                    } else {
                        goBack();
                    }
                    break;
            }
        });
        
        // Detectar cambios en fullscreen
        document.addEventListener('fullscreenchange', () => {
            isFullscreen = !!document.fullscreenElement;
        });
        
        // Ocultar controles después de inactividad
        let hideControlsTimeout;
        function resetHideControlsTimeout() {
            clearTimeout(hideControlsTimeout);
            hideControlsTimeout = setTimeout(() => {
                if (isPlaying) {
                    document.querySelector('.video-controls').style.transform = 'translateY(100%)';
                    document.querySelector('.video-title').style.opacity = '0';
                    document.querySelector('.navigation-buttons').style.opacity = '0';
                }
            }, 3000);
        }
        
        videoContainer.addEventListener('mousemove', () => {
            document.querySelector('.video-controls').style.transform = 'translateY(0)';
            document.querySelector('.video-title').style.opacity = '1';
            document.querySelector('.navigation-buttons').style.opacity = '1';
            resetHideControlsTimeout();
        });
        
        // Inicializar
        resetHideControlsTimeout();
    </script>
</body>
</html>
"""
