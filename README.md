# sing_language_escritorio# Sistema de Reconocimiento de Lenguaje de Señas 👋

![Interfaz Principal](screenshots/main_interface.png)  
*Interfaz interactiva del sistema*

## 📌 Descripción
Aplicación de escritorio para **aprender, practicar y detectar lenguaje de señas** en tiempo real usando IA. Incluye:

- 🔍 **Detector de señas** con modelo Random Forest entrenado
- 🅰️ **Abecedario completo** con demostraciones visuales
- 📖 **Diccionario de palabras** comunes
- ✏️ **Modo práctica** para deletrear palabras
- 🎤 **Sistema de audio** integrado

## 🚀 Características Principales
| Módulo | Funcionalidad |
|--------|--------------|
| **Detección en Tiempo Real** | Reconocimiento de gestos con cámara usando OpenCV + MediaPipe |
| **Abecedario Interactivo** | Visualización de cada letra con imágenes/videos demostrativos |
| **Buscador de Palabras** | Desglose de palabras en señas individuales |
| **Modo Práctica** | Ejercicios guiados para formación de palabras |
| **IA Integrada** | Modelo Random Forest (precisión del 92% en pruebas) |
| **Feedback Auditivo** | Pronunciación de letras/palabras detectadas |

## 🛠️ Tecnologías
```python
Python 3.9+
PyQt5        # Interfaz gráfica
OpenCV       # Procesamiento de video
MediaPipe    # Detección de landmarks
Scikit-learn # Modelo Random Forest
Joblib       # Serialización del modelo
pyttsx3      # Texton a voz


## 🛠️ LIbrerias de instalacion (comandos):
pip install PyQt5
pip install opencv-python
pip install mediapipe
pip install scikit-learn
pip install joblib
pip install pyttsx3
pip install numpy
pip install msvc-runtime (solo para windows, evitar errores de dependencias)

## Instalacion y Ejecucion
1. Clonar el repositorio:
git clone https://github.com/PollitoJLGD123/sing_language_escritorio.git
2. Instalar las librerias anteriormente mencionadas
3. Ejecutar el archivo main.py de esta manera: python main.py
