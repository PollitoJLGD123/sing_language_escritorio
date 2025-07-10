from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QLabel, QVBoxLayout, QHBoxLayout, 
    QPushButton, QFrame, QGridLayout, QSpacerItem, QSizePolicy,
    QScrollArea, QProgressBar
)
from PyQt5.QtGui import QFont, QPixmap, QPainter, QLinearGradient, QBrush, QColor
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
import random
import cv2
from PyQt5.QtGui import QImage, QPixmap, QFont
import numpy as np
import joblib
import mediapipe as mp



class GradientLabel(QLabel):
    """Label con gradiente personalizado"""
    def __init__(self, text="", colors=None, parent=None):
        super().__init__(text, parent)
        self.gradient_colors = colors or [(138, 43, 226), (33, 150, 243)]
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        gradient = QLinearGradient(0, 0, self.width(), 0)
        for i, color in enumerate(self.gradient_colors):
            gradient.setColorAt(i / (len(self.gradient_colors) - 1), QColor(*color))
        
        painter.fillRect(self.rect(), QBrush(gradient))
        
        # Sombra del texto
        painter.setPen(QColor(0, 0, 0, 80))
        painter.drawText(self.rect().adjusted(2, 2, 2, 2), self.alignment(), self.text())
        
        # Texto principal
        painter.setPen(QColor(255, 255, 255))
        painter.drawText(self.rect(), self.alignment(), self.text())

class StyledButton(QPushButton):
    """Botón personalizado con estilos"""
    def __init__(self, text="", button_type="primary", parent=None):
        super().__init__(text, parent)
        self.setFont(QFont("Comic Sans MS", 14, QFont.Bold))
        self.setMinimumHeight(50)
        
        if button_type == "primary":
            self.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #4CAF50, stop:1 #2196F3);
                    color: white;
                    border: none;
                    border-radius: 25px;
                    padding: 12px 24px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #45A049, stop:1 #1976D2);
                    transform: translateY(-2px);
                }
                QPushButton:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #3D8B40, stop:1 #1565C0);
                }
            """)
        elif button_type == "danger":
            self.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #F44336, stop:1 #E91E63);
                    color: white;
                    border: none;
                    border-radius: 25px;
                    padding: 12px 24px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #D32F2F, stop:1 #C2185B);
                    transform: translateY(-2px);
                }
                QPushButton:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #B71C1C, stop:1 #AD1457);
                }
            """)
        elif button_type == "secondary":
            self.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #9C27B0, stop:1 #673AB7);
                    color: white;
                    border: none;
                    border-radius: 25px;
                    padding: 12px 24px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #7B1FA2, stop:1 #512DA8);
                    transform: translateY(-2px);
                }
                QPushButton:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #6A1B9A, stop:1 #4527A0);
                }
            """)

class InfoCard(QFrame):
    """Tarjeta de información estilizada"""
    def __init__(self, title, content_widget, card_type="default", parent=None):
        super().__init__(parent)
        self.setupUI(title, content_widget, card_type)
        
    def setupUI(self, title, content_widget, card_type):
        # Estilos según el tipo de tarjeta
        if card_type == "challenge":
            bg_gradient = "stop:0 rgba(156, 39, 176, 0.1), stop:1 rgba(233, 30, 99, 0.05)"
            border_color = "#E1BEE7"
        elif card_type == "result_correct":
            bg_gradient = "stop:0 rgba(76, 175, 80, 0.1), stop:1 rgba(129, 199, 132, 0.05)"
            border_color = "#C8E6C9"
        elif card_type == "result_incorrect":
            bg_gradient = "stop:0 rgba(244, 67, 54, 0.1), stop:1 rgba(255, 138, 128, 0.05)"
            border_color = "#FFCDD2"
        elif card_type == "camera":
            bg_gradient = "stop:0 rgba(33, 150, 243, 0.1), stop:1 rgba(156, 39, 176, 0.05)"
            border_color = "#BBDEFB"
        else:
            bg_gradient = "stop:0 rgba(255, 255, 255, 0.9), stop:1 rgba(248, 250, 255, 0.8)"
            border_color = "#E0E0E0"
        
        self.setFrameStyle(QFrame.NoFrame)
        self.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, {bg_gradient});
                border: 3px solid {border_color};
                border-radius: 20px;
                margin: 2px;
                padding: 1px;
            }}
        """)
        
        # Layout principal
        layout = QVBoxLayout()  
        # Contenido
        layout.addWidget(content_widget)
        self.setLayout(layout)

class ChallengeWidget(QWidget):
    """Widget para mostrar el desafío actual"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_letter = "A"
        self.setupUI()
        
    def setupUI(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)
        
        # Letra grande
        self.letter_label = QLabel(self.current_letter)
        self.letter_label.setFont(QFont("Comic Sans MS", 80, QFont.Bold))
        self.letter_label.setAlignment(Qt.AlignCenter)
        self.letter_label.setStyleSheet("""
            QLabel {
                color: #7B1FA2;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(255, 255, 255, 0.9), 
                    stop:1 rgba(248, 250, 255, 0.7));
                border-radius: 15px;
                padding: 20px;
                border: 3px solid rgba(156, 39, 176, 0.3);
                min-height: 120px;
            }
        """)
        
        # Imagen de la seña
        self.sign_image = QLabel()
        self.sign_image.setAlignment(Qt.AlignCenter)
        self.sign_image.setStyleSheet("""
            QLabel {
                background: rgba(255, 255, 255, 0.8);
                border-radius: 15px;
                padding: 15px;
                border: 2px solid rgba(156, 39, 176, 0.2);
                min-height: 100px;
                min-width: 100px;
            }
        """)
        
        # Cargar imagen o emoji de fallback
        pixmap = QPixmap(f"images/utils/{self.current_letter.lower()}.jpg")
        if not pixmap.isNull():
            pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.sign_image.setPixmap(pixmap)
        else:
            self.sign_image.setText("🤟")
            self.sign_image.setFont(QFont("Arial", 50))
            self.sign_image.setStyleSheet(self.sign_image.styleSheet() + "color: #9C27B0;")
        
        # Instrucción
        instruction = QLabel(f'Haz la seña para "{self.current_letter}" frente a la cámara')
        instruction.setFont(QFont("Comic Sans MS", 14))
        instruction.setAlignment(Qt.AlignCenter)
        instruction.setWordWrap(True)
        instruction.setStyleSheet("""
            QLabel {
                color: #424242;
                background: rgba(255, 255, 255, 0.5);
                border-radius: 10px;
                padding: 10px;
            }
        """)
        
        layout.addWidget(self.letter_label)
        layout.addWidget(self.sign_image)
        layout.addWidget(instruction)
        
        self.setLayout(layout)
    
    def update_challenge(self, letter):
        """Actualizar el desafío con una nueva letra"""
        self.current_letter = letter
        self.letter_label.setText(letter)
        
        # Actualizar imagen
        pixmap = QPixmap(f"images/utils/{letter.lower()}.jpg")
        if not pixmap.isNull():
            pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.sign_image.setPixmap(pixmap)
        else:
            self.sign_image.setText("🤟")

class ResultWidget(QWidget):
    """Widget para mostrar resultados de detección"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.prediction = None
        self.is_correct = None
        self.setupUI()
        
    def setupUI(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)
        
        # Estado inicial
        self.status_icon = QLabel("🤖")
        self.status_icon.setFont(QFont("Arial", 60))
        self.status_icon.setAlignment(Qt.AlignCenter)
        
        self.result_text = QLabel("Esperando...")
        self.result_text.setFont(QFont("Comic Sans MS", 18, QFont.Bold))
        self.result_text.setAlignment(Qt.AlignCenter)
        self.result_text.setStyleSheet("color: #666666;")
        
        self.detail_text = QLabel("Activa la cámara y haz una seña para comenzar")
        self.detail_text.setFont(QFont("Comic Sans MS", 12))
        self.detail_text.setAlignment(Qt.AlignCenter)
        self.detail_text.setWordWrap(True)
        self.detail_text.setStyleSheet("color: #888888;")
        
        # Botón de reintentar (inicialmente oculto)
        self.retry_button = StyledButton("🔄 Intentar de nuevo", "secondary")
        self.retry_button.hide()
        
        layout.addWidget(self.status_icon)
        layout.addWidget(self.result_text)
        layout.addWidget(self.detail_text)
        layout.addWidget(self.retry_button)
        
        self.setLayout(layout)
    
    def update_result(self, prediction, is_correct):
        """Actualizar el resultado de la detección"""
        self.prediction = prediction
        self.is_correct = is_correct
        
        if is_correct:
            self.status_icon.setText("✅")
            self.result_text.setText(f"{prediction}")
            self.result_text.setStyleSheet("color: #4CAF50; font-size: 24px;")
            self.detail_text.setText("¡Excelente trabajo! ¡Sigue así!")
            self.detail_text.setStyleSheet("color: #2E7D32;")
            self.retry_button.hide()
        else:
            self.status_icon.setText("❌")
            self.result_text.setText(f"{prediction}")
            self.result_text.setStyleSheet("color: #F44336; font-size: 24px;")
            self.detail_text.setText("Sigue intentando, ¡tú puedes!")
            self.detail_text.setStyleSheet("color: #C62828;")
            self.retry_button.show()
    
    def reset_result(self):
        """Resetear el resultado"""
        self.prediction = None
        self.is_correct = None
        self.status_icon.setText("🤖")
        self.result_text.setText("Esperando detección...")
        self.result_text.setStyleSheet("color: #666666; font-size: 18px;")
        self.detail_text.setText("Haz una seña frente a la cámara")
        self.detail_text.setStyleSheet("color: #888888;")
        self.retry_button.hide()


class CameraWidget(QWidget):
    """Widget para la cámara con detección de señas"""
    detection_signal = pyqtSignal(str)  # Señal que envía la letra detectada
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_camera_active = False
        self.cap = None
        self.timer = QTimer()
        self.current_prediction = ""
        self.prediction_confidence = 0
        self.palabra = ""
        
        # Cargar modelo y encoder
        self.model = joblib.load('src/model/modelo.joblib')
        self.encoder = joblib.load('src/model/labels.joblib')
        
        # Configurar MediaPipe
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=True,
            min_detection_confidence=0.5
        )
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        
        self.setupUI()
        
    def setupUI(self):
        layout = QVBoxLayout()
        
        # Área de la cámara
        self.camera_area = QLabel()
        self.camera_area.setAlignment(Qt.AlignCenter)
        self.camera_area.setMinimumSize(640, 480)
        self.camera_area.setStyleSheet("""
            QLabel {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1a1a1a, stop:1 #2d2d2d);
                border-radius: 15px;
                border: 3px solid #333333;
                color: #888888;
                font-size: 16px;
            }
        """)
        
        # Estado inicial de la cámara
        self.update_camera_display()
        
        # Controles de la cámara
        controls_layout = QHBoxLayout()
        controls_layout.setAlignment(Qt.AlignCenter)
        controls_layout.setSpacing(15)
        
        self.start_camera_btn = StyledButton("📹 Activar Cámara", "primary")
        self.stop_camera_btn = StyledButton("📹 Desactivar", "danger")
        self.detect_btn = StyledButton("🔍 Detectar Seña", "secondary")
        self.clear_btn = StyledButton("🧹 Limpiar", "warning")
        
        # Conectar botones
        self.start_camera_btn.clicked.connect(self.start_camera)
        self.stop_camera_btn.clicked.connect(self.stop_camera)
        self.detect_btn.clicked.connect(self.toggle_detection)
        self.clear_btn.clicked.connect(self.clear_word)
        
        # Inicialmente solo mostrar el botón de activar
        self.stop_camera_btn.hide()
        self.detect_btn.hide()
        self.clear_btn.hide()
        
        controls_layout.addWidget(self.start_camera_btn)
        controls_layout.addWidget(self.stop_camera_btn)
        controls_layout.addWidget(self.detect_btn)
        controls_layout.addWidget(self.clear_btn)
        
        # Área de visualización de la palabra
        self.word_display = QLabel("Palabra: ")
        self.word_display.setFont(QFont("Comic Sans MS", 14))
        self.word_display.setAlignment(Qt.AlignCenter)
        self.word_display.setStyleSheet("""
            QLabel {
                color: #FFFFFF;
                background: rgba(30, 30, 30, 0.7);
                border-radius: 10px;
                padding: 10px;
                border: 2px solid #444444;
            }
        """)
        self.word_display.hide()
        
        # Info de la cámara
        camera_info = QLabel("Resolución: 640x480 | Asegúrate de tener buena iluminación")
        camera_info.setFont(QFont("Comic Sans MS", 11))
        camera_info.setAlignment(Qt.AlignCenter)
        camera_info.setStyleSheet("""
            QLabel {
                color: #666666;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 10px;
                padding: 8px;
            }
        """)
        
        layout.addWidget(self.camera_area)
        layout.addWidget(self.word_display)
        layout.addLayout(controls_layout)
        layout.addWidget(camera_info)
        
        self.setLayout(layout)
    
    def start_camera(self):
        """Iniciar la cámara y detección"""
        if not self.is_camera_active:
            self.cap = cv2.VideoCapture(0)
            
            if not self.cap.isOpened():
                self.camera_area.setText("⚠️ Error al abrir la cámara")
                return
            
            self.is_camera_active = True
            self.start_camera_btn.hide()
            self.stop_camera_btn.show()
            self.detect_btn.show()
            self.clear_btn.show()
            self.word_display.show()
            
            # Configurar timer para actualizar frames
            self.timer.timeout.connect(self.update_frame)
            self.timer.start(30)  # ~33 FPS
            
            # Actualizar estilo
            self.camera_area.setStyleSheet("""
                QLabel {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 #0d4f3c, stop:1 #1a5f4a);
                    border-radius: 15px;
                    border: 3px solid #4CAF50;
                    color: #A5D6A7;
                    font-size: 14px;
                }
            """)
    
    def stop_camera(self):
        """Detener la cámara"""
        if self.is_camera_active:
            self.timer.stop()
            if self.cap:
                self.cap.release()
            
            self.is_camera_active = False
            self.start_camera_btn.show()
            self.stop_camera_btn.hide()
            self.detect_btn.hide()
            self.clear_btn.hide()
            self.word_display.hide()
            self.update_camera_display()
    
    def toggle_detection(self):
        """Alternar el modo de detección"""
        self.is_detection_active = not getattr(self, 'is_detection_active', False)
        if self.is_detection_active:
            self.detect_btn.setStyleSheet("background-color: #4CAF50; color: white;")
        else:
            self.detect_btn.setStyleSheet("")  # Volver al estilo original
    
    def clear_word(self):
        """Limpiar la palabra acumulada"""
        self.palabra = ""
        self.word_display.setText("Palabra: ")
    
    def update_frame(self):
        """Procesar cada frame de la cámara"""
        ret, frame = self.cap.read()
        if not ret:
            return

        # Procesamiento con MediaPipe solo si la detección está activa
        if getattr(self, 'is_detection_active', False):
            frame, prediction = self.process_hands(frame)
            if prediction:
                self.current_prediction = prediction[0]
                self.prediction_confidence = prediction[1]
                self.word_display.setText(f"Palabra: {self.palabra}{self.current_prediction}")
                self.detection_signal.emit(self.current_prediction)
        
        # Convertir el frame para mostrarlo en Qt
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        
        # Mostrar en el QLabel
        pixmap = QPixmap.fromImage(qt_image)
        self.camera_area.setPixmap(
            pixmap.scaled(
                self.camera_area.width(),
                self.camera_area.height(),
                Qt.KeepAspectRatio,
            )
        )
    
    def process_hands(self, frame):
        """Procesar la detección de manos y realizar predicción"""
        data_aux = []
        x_ = []
        y_ = []
        
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(frame_rgb)
        
        prediction = None
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Dibujar landmarks y conexiones
                self.mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_drawing_styles.get_default_hand_landmarks_style(),
                    self.mp_drawing_styles.get_default_hand_connections_style())
                
                # Recopilar coordenadas
                for landmark in hand_landmarks.landmark:
                    x_.append(landmark.x)
                    y_.append(landmark.y)
                
                # Normalizar coordenadas
                for i in range(len(hand_landmarks.landmark)):
                    x = hand_landmarks.landmark[i].x
                    y = hand_landmarks.landmark[i].y
                    data_aux.append(x - min(x_))
                    data_aux.append(y - min(y_))
                
                # Dibujar cuadro delimitador
                h, w, _ = frame.shape
                margen = 20
                x1 = max(0, int(min(x_) * w) - margen)
                y1 = max(0, int(min(y_) * h) - margen)
                x2 = min(w, int(max(x_) * w) + margen)
                y2 = min(h, int(max(y_) * h) + margen)
                
                # Realizar predicción
                try:
                    prediction = self.model.predict([np.asarray(data_aux)])
                    predicted_char = self.encoder.inverse_transform(prediction)[0].decode('utf-8')
                    prediction_proba = self.model.predict_proba([np.asarray(data_aux)])
                    confidence = prediction_proba.max() * 100
                    
                    # Dibujar información de la predicción
                    overlay = frame.copy()
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (100, 255, 0), 4)
                    cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)
                    
                    # Barra de confianza
                    bar_x1, bar_y1 = x1, y1 - 20
                    bar_x2, bar_y2 = x1 + int((x2 - x1) * (confidence / 100)), y1 - 10
                    cv2.rectangle(frame, (bar_x1, bar_y1), (bar_x2, bar_y2), (0, 255, 0), -1)
                    
                    # Texto de predicción
                    cv2.putText(frame, f"{predicted_char} ({confidence:.2f}%)",
                                (x1 + 5, y1 - 30),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.8, (155, 155, 30), 2, cv2.LINE_AA)
                    
                    prediction = (predicted_char, confidence)
                    
                except Exception as e:
                    print(f"Error en predicción: {e}")
                    prediction = None
        
        return frame, prediction
    
    def update_camera_display(self):
        """Mostrar mensaje cuando la cámara está desactivada"""
        self.camera_area.setText("""
            📹
            
            Cámara desactivada
            
            Haz clic en "Activar Cámara" para comenzar
        """)
        self.camera_area.setFont(QFont("Comic Sans MS", 16))
        self.camera_area.setStyleSheet("""
            QLabel {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1a1a1a, stop:1 #2d2d2d);
                border-radius: 15px;
                border: 3px solid #333333;
                color: #888888;
                font-size: 16px;
            }
        """)
    
    def closeEvent(self, event):
        """Liberar recursos al cerrar"""
        self.stop_camera()
        if hasattr(self, 'hands'):
            self.hands.close()
        event.accept()

def page_practice():
    """Página principal de práctica"""
    
    # Widget principal con scroll
    scroll_area = QScrollArea()
    scroll_area.setWidgetResizable(True)
    scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
    scroll_area.setStyleSheet("""
        QScrollArea {
            border: none;
            background: transparent;
        }
        QScrollBar:vertical {
            background: rgba(255, 255, 255, 0.1);
            width: 12px;
            border-radius: 6px;
        }
        QScrollBar::handle:vertical {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #9C27B0, stop:1 #2196F3);
            border-radius: 6px;
            min-height: 20px;
        }
    """)
    
    # Widget de contenido
    content_widget = QWidget()
    content_widget.setStyleSheet("""
        QWidget {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #F8F9FF, stop:0.3 #E8F4FD, 
                stop:0.6 #F0F8E8, stop:1 #FFF0E6);
            font-family: 'Comic Sans MS';
        }
    """)
    
    # Layout principal
    main_layout = QVBoxLayout()
    main_layout.setSpacing(30)
    main_layout.setContentsMargins(30, 30, 30, 30)
    
    # === HEADER ===
    header_layout = QVBoxLayout()
    header_layout.setAlignment(Qt.AlignCenter)
    header_layout.setSpacing(15)
    
    # Título principal
    title = GradientLabel("🎯 Zona de Práctica 🎯", [(138, 43, 226), (33, 150, 243)])
    title.setFont(QFont("Comic Sans MS", 32, QFont.Bold))
    title.setAlignment(Qt.AlignCenter)
    title.setMinimumHeight(80)
    title.setStyleSheet("border-radius: 20px; margin: 10px;")
    
    # Subtítulo
    subtitle = QLabel("Activa tu cámara y practica las señas. ¡El sistema te dará retroalimentación en tiempo real!")
    subtitle.setFont(QFont("Comic Sans MS", 16))
    subtitle.setAlignment(Qt.AlignCenter)
    subtitle.setWordWrap(True)
    subtitle.setStyleSheet("""
        QLabel {
            color: #424242;
            background: rgba(255, 255, 255, 0.7);
            border-radius: 15px;
            padding: 15px;
            margin: 10px;
        }
    """)
    
    header_layout.addWidget(title)
    header_layout.addWidget(subtitle)
    
    # === PUNTOS Y DESAFÍO ACTUAL ===
    stats_layout = QHBoxLayout()
    stats_layout.setAlignment(Qt.AlignCenter)
    stats_layout.setSpacing(20)
    
    # Puntos
    points_label = QLabel("🏆 Puntos: 0")
    points_label.setFont(QFont("Comic Sans MS", 16, QFont.Bold))
    points_label.setStyleSheet("""
        QLabel {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #4CAF50, stop:1 #2196F3);
            color: white;
            border-radius: 20px;
            padding: 12px 24px;
            border: 2px solid rgba(255, 255, 255, 0.3);
        }
    """)
    
    # Desafío actual
    challenge_label = QLabel("🎯 Practica: A")
    challenge_label.setFont(QFont("Comic Sans MS", 16, QFont.Bold))
    challenge_label.setStyleSheet("""
        QLabel {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #9C27B0, stop:1 #E91E63);
            color: white;
            border-radius: 20px;
            padding: 12px 24px;
            border: 2px solid rgba(255, 255, 255, 0.3);
        }
    """)
    
    stats_layout.addWidget(points_label)
    stats_layout.addWidget(challenge_label)
    
    # === LAYOUT PRINCIPAL DE CONTENIDO ===
    content_layout = QHBoxLayout()
    content_layout.setSpacing(30)
    
    # === COLUMNA IZQUIERDA: CONTROLES Y MÉTRICAS ===
    left_column = QVBoxLayout()
    
    # Layout para las cards
    cards_layout = QHBoxLayout()
    cards_layout.setSpacing(20)  # Añadir espacio entre las cards
    
    # Tarjeta de desafío actual
    challenge_widget = ChallengeWidget()
    challenge_card = InfoCard("🎯 Seña a Practicar", challenge_widget, "challenge")
    challenge_card.setMinimumWidth(400)
    challenge_card.setMaximumWidth(500)
    
    # Tarjeta de resultado
    result_widget = ResultWidget()
    result_card = InfoCard("🤖 Resultado de la Detección", result_widget, "default")
    result_card.setMinimumWidth(400)
    result_card.setMaximumWidth(500)
    
    # Añadir las cards al layout horizontal
    cards_layout.addWidget(challenge_card)
    cards_layout.addWidget(result_card)
    
    # Botón siguiente desafío
    next_challenge_btn = StyledButton("➡️ Siguiente Desafío", "secondary")
    next_challenge_btn.setMinimumWidth(500)
    next_challenge_btn.setMaximumWidth(500)
    
    # Añadir el layout de las cards y el botón al layout principal
    left_column.addLayout(cards_layout)
    left_column.addWidget(next_challenge_btn)
    left_column.addStretch()
    
    # === COLUMNA DERECHA: CÁMARA ===
    camera_widget = CameraWidget()
    camera_card = InfoCard("📹 Cámara de Práctica", camera_widget, "camera")
    camera_card.setMaximumHeight(700)
    
    # === ENSAMBLAR COLUMNAS ===
    content_layout.addLayout(left_column, 2)  # 40% del ancho
    content_layout.addWidget(camera_card, 2)   # 60% del ancho
    
    # === ENSAMBLAR TODO ===
    main_layout.addLayout(header_layout)
    main_layout.addLayout(stats_layout)
    main_layout.addLayout(content_layout)
    main_layout.addStretch()
    
    content_widget.setLayout(main_layout)
    scroll_area.setWidget(content_widget)
        
    letters = ['A', 'B', 'C', 'D', 'E']
    detected = random.choice(letters)
    is_correct = detected == challenge_widget.current_letter
    result_widget.update_result(detected, is_correct)
    print(f"Detectado: {detected}, Correcto: {is_correct}")
    
    def on_next_challenge():
        # Cambiar a la siguiente letra
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        new_letter = random.choice(letters)
        challenge_widget.update_challenge(new_letter)
        challenge_label.setText(f"🎯 Practica: {new_letter}")
        result_widget.reset_result()
        print(f"Nuevo desafío: {new_letter}")
    
    def on_retry():
        result_widget.reset_result()
        print("Reintentando...")
    

    next_challenge_btn.clicked.connect(on_next_challenge)
    result_widget.retry_button.clicked.connect(on_retry)
    
    return scroll_area