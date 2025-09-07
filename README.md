# 🎬 Call Of The NIGHT - Servidor de Video Streaming

Un servidor de video streaming personalizado con interfaz estilo Netflix, diseñado para reproducir series y películas desde tu computadora local.

## ✨ Características

- **Interfaz estilo Netflix** con miniaturas y progreso visual
- **Auto-avance inteligente** entre capítulos
- **Sistema de progreso** que recuerda dónde dejaste cada video
- **Reproductor optimizado para TV** con controles por teclado
- **Configuración flexible** mediante archivo `.env`
- **Ordenamiento numérico** de capítulos (cap1, cap2, cap10...)

## 🚀 Instalación

1. **Clona o descarga** este proyecto
2. **Instala las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configura el archivo `.env`:**
   - Copia `env_example.txt` como `.env`
   - Modifica la ruta de tus videos en `VIDEO_PATH`
   - Ajusta otros parámetros según necesites

4. **Ejecuta el servidor:**
   ```bash
   python main.py
   ```

## ⚙️ Configuración

### Archivo `.env`

```env
# Título de la aplicación
APP_TITLE=Call Of The NIGHT

# Puerto del servidor
PORT=5000

# IP del servidor (0.0.0.0 para acceso desde cualquier dispositivo)
HOST=0.0.0.0

# Ruta donde están tus videos
VIDEO_PATH=D:\Mis Documentos\Call Of The NIGHT

# Configuración de auto-avance
AUTO_ADVANCE_TRIGGER_SECONDS=100  # 1 minuto 40 segundos
AUTO_ADVANCE_COUNTDOWN_SECONDS=15 # 15 segundos de countdown

# Intervalo para guardar progreso (segundos)
PROGRESS_SAVE_INTERVAL=10

# Directorio de miniaturas
THUMBNAIL_CACHE_DIR=thumbnails_cache

# Modo debug
DEBUG=True
```

### Rutas de Video

- **Windows:** `D:\\Mis Documentos\\Call Of The NIGHT`
- **Linux/Mac:** `/home/usuario/videos`

## 🎮 Controles

### En el Reproductor
- **Click en el video** - Pausar/Reproducir
- **Click en la barra de progreso** - Saltar a esa posición
- **Hover en la barra** - Ver preview del tiempo
- **Espacio/Enter** - Pausar/Reproducir
- **Flechas ← →** - Video anterior/siguiente
- **F** - Pantalla completa
- **Esc** - Salir de pantalla completa

### En la Lista Principal
- **Click en video** - Abrir en nueva pestaña
- **Regenerar Miniaturas** - Crear nuevas miniaturas
- **Actualizar Progreso** - Sincronizar progreso

## 📁 Estructura de Archivos

```
SERVER SERIES/
├── main.py                 # Punto de entrada
├── config.py              # Configuración
├── routes.py              # Rutas del servidor
├── utils.py               # Utilidades
├── templates.py           # Template principal
├── video_player_template.py # Template del reproductor
├── thumbnails.py          # Generación de miniaturas
├── progress.py            # Sistema de progreso
├── requirements.txt       # Dependencias
├── .env                   # Configuración (crear desde env_example.txt)
└── thumbnails_cache/      # Cache de miniaturas (se crea automáticamente)
```

## 🔧 Personalización

### Cambiar Tiempo de Auto-avance
Edita en `.env`:
```env
AUTO_ADVANCE_TRIGGER_SECONDS=120  # 2 minutos antes del final
AUTO_ADVANCE_COUNTDOWN_SECONDS=10 # 10 segundos de countdown
```

### Cambiar Título de la Aplicación
```env
APP_TITLE=Mi Servidor de Videos  # Cambiar el título
```

### Cambiar Puerto
```env
PORT=8080  # Cambiar a puerto 8080
```

### Desactivar Debug
```env
DEBUG=False
```

## 🌐 Acceso

Una vez iniciado el servidor:

- **Local:** `http://localhost:5000`
- **Desde TV/otros dispositivos:** `http://TU_IP_LOCAL:5000`

La IP local se muestra al iniciar el servidor.

## 🎯 Características Avanzadas

### Sistema de Progreso
- Guarda automáticamente el progreso cada 10 segundos
- Muestra barras rojas en las miniaturas
- Reanuda desde donde dejaste

### Miniaturas Inteligentes
- Se generan automáticamente
- Usan frames aleatorios del video (no siempre el inicio)
- Se cachean para mejor rendimiento

### Auto-avance Netflix
- Notificación antes del final
- Countdown configurable
- Opción de cancelar o acelerar

## 🐛 Solución de Problemas

### Error de NumPy
```bash
pip install "numpy<2.0" --force-reinstall
```

### Videos no aparecen
- Verifica la ruta en `VIDEO_PATH`
- Asegúrate de que los archivos tengan extensiones soportadas
- Revisa permisos de lectura

### Miniaturas no se generan
- Instala OpenCV: `pip install opencv-python`
- Verifica que los videos no estén corruptos

## 📝 Notas

- Compatible con Windows, Linux y macOS
- Optimizado para uso en TV con control remoto
- Soporta múltiples formatos de video
- Sistema de progreso persistente

¡Disfruta tu experiencia de streaming personalizada! 🎬✨
