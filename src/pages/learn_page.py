from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QGridLayout, 
    QFrame, QScrollArea, QPushButton, QSpacerItem, QSizePolicy
)
from PyQt5.QtGui import QFont, QPixmap, QPainter, QLinearGradient, QBrush, QColor
from PyQt5.QtCore import Qt

# Lista de letras del abecedario
list_letters = [
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", 
    "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "space"
]

# Lista de palabras básicas
basic_words = [
    {"word": "hola", "display": "Hola", "description": "Saludo amistoso"},
    {"word": "gracias", "display": "Gracias", "description": "Expresar gratitud"},
    {"word": "por_favor", "display": "Por Favor", "description": "Pedir algo educadamente"},
    {"word": "si", "display": "Sí", "description": "Respuesta afirmativa"},
    {"word": "no", "display": "No", "description": "Respuesta negativa"},
    {"word": "agua", "display": "Agua", "description": "Líquido vital"},
    {"word": "comer", "display": "Comer", "description": "Acción de alimentarse"},
    {"word": "dormir", "display": "Dormir", "description": "Descansar por la noche"},
    {"word": "jugar", "display": "Jugar", "description": "Divertirse y entretenerse"},
    {"word": "familia", "display": "Familia", "description": "Personas que nos aman"},
    {"word": "escuela", "display": "Escuela", "description": "Lugar de aprendizaje"},
    {"word": "amigo", "display": "Amigo", "description": "Persona especial"}
]

class GradientTitleLabel(QLabel):
    """Título con gradiente personalizado"""
    def __init__(self, text="", colors=None, parent=None):
        super().__init__(text, parent)
        self.gradient_colors = colors or [(255, 107, 157), (156, 39, 176), (33, 150, 243)]
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Crear gradiente
        gradient = QLinearGradient(0, 0, self.width(), 0)
        for i, color in enumerate(self.gradient_colors):
            gradient.setColorAt(i / (len(self.gradient_colors) - 1), QColor(*color))
        
        # Dibujar fondo con gradiente
        painter.fillRect(self.rect(), QBrush(gradient))
        
        # Dibujar texto con sombra
        painter.setPen(QColor(0, 0, 0, 80))
        painter.drawText(self.rect().adjusted(2, 2, 2, 2), self.alignment(), self.text())
        
        painter.setPen(QColor(255, 255, 255))
        painter.drawText(self.rect(), self.alignment(), self.text())

class LetterCard(QFrame):
    """Tarjeta mejorada para mostrar letras"""
    def __init__(self, letter, parent=None):
        super().__init__(parent)
        self.letter = letter
        self.setupUI()
        
    def setupUI(self):
        # Estilo de la tarjeta
        self.setFrameStyle(QFrame.NoFrame)
        self.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(255, 255, 255, 0.95), 
                    stop:1 rgba(248, 250, 255, 0.9));
                border: 3px solid qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #E1BEE7, stop:1 #BBDEFB);
                border-radius: 15px;
                margin: 8px;
                padding: 5px;
            }
            QFrame:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(156, 39, 176, 0.1), 
                    stop:1 rgba(33, 150, 243, 0.1));
                border: 3px solid #9C27B0;
                transform: scale(1.05);
            }
        """)
        
        # Layout de la tarjeta
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setAlignment(Qt.AlignCenter)
        
        # Etiqueta de la letra
        letter_display = self.letter.upper() if self.letter != "space" else "ESPACIO"
        letter_label = QLabel(letter_display)
        letter_label.setFont(QFont("Comic Sans MS", 20, QFont.Bold))
        letter_label.setAlignment(Qt.AlignCenter)
        letter_label.setStyleSheet("""
            QLabel {
                color: #4A148C;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #FFE0F0, stop:1 #E8F4FD);
                border-radius: 10px;
                padding: 8px;
                margin: 5px;
                border: 2px solid rgba(156, 39, 176, 0.3);
            }
        """)
        
        # Imagen de la letra
        image_label = QLabel()
        image_label.setAlignment(Qt.AlignCenter)
        image_label.setStyleSheet("""
            QLabel {
                background: rgba(255, 255, 255, 0.5);
                border-radius: 10px;
                padding: 10px;
                border: 2px solid rgba(33, 150, 243, 0.2);
            }
        """)
        image_label.setFixedSize(150, 150)
        
        # Cargar imagen
        pixmap = QPixmap(f"images/utils/{self.letter.lower()}.jpg")
        if pixmap.isNull():
            # Imagen de respaldo
            pixmap = QPixmap(f"images/utils/a.jpg")
        
        if not pixmap.isNull():
            pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            image_label.setPixmap(pixmap)
        else:
            # Si no hay imagen, mostrar emoji
            image_label.setText("🤟")
            image_label.setFont(QFont("Arial", 60))
            image_label.setStyleSheet(image_label.styleSheet() + "color: #9C27B0;")
        
        # Agregar elementos al layout
        layout.addWidget(letter_label)
        layout.addWidget(image_label)
        
        self.setLayout(layout)
        self.setFixedSize(200, 300)

class WordCard(QFrame):
    """Tarjeta para mostrar palabras básicas"""
    def __init__(self, word_data, parent=None):
        super().__init__(parent)
        self.word_data = word_data
        self.setupUI()
        
    def setupUI(self):
        # Estilo de la tarjeta
        self.setFrameStyle(QFrame.NoFrame)
        self.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(255, 255, 255, 0.95), 
                    stop:1 rgba(240, 248, 235, 0.9));
                border: 3px solid qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #C8E6C9, stop:1 #81C784);
                border-radius: 15px;
                margin: 8px;
                padding: 5px;
            }
            QFrame:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(76, 175, 80, 0.1), 
                    stop:1 rgba(129, 199, 132, 0.1));
                border: 3px solid #4CAF50;
                transform: scale(1.05);
            }
        """)
        
        # Layout de la tarjeta
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setAlignment(Qt.AlignCenter)
        
        # Título de la palabra
        word_label = QLabel(self.word_data["display"])
        word_label.setFont(QFont("Comic Sans MS", 18, QFont.Bold))
        word_label.setAlignment(Qt.AlignCenter)
        word_label.setStyleSheet("""
            QLabel {
                color: #1B5E20;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #E8F5E8, stop:1 #F1F8E9);
                border-radius: 10px;
                padding: 8px;
                margin: 5px;
                border: 2px solid rgba(76, 175, 80, 0.3);
            }
        """)
        
        # Imagen de la palabra
        image_label = QLabel()
        image_label.setAlignment(Qt.AlignCenter)
        image_label.setStyleSheet("""
            QLabel {
                background: rgba(255, 255, 255, 0.5);
                border-radius: 10px;
                padding: 10px;
                border: 2px solid rgba(76, 175, 80, 0.2);
            }
        """)
        
        image_label.setFixedSize(150, 150)
        
        # Cargar imagen
        pixmap = QPixmap(f"images/words/{self.word_data['word']}.jpg")
        if pixmap.isNull():
            # Imagen de respaldo
            pixmap = QPixmap(f"images/words/hola.jpg")
        
        if not pixmap.isNull():
            pixmap = pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            image_label.setPixmap(pixmap)
        else:
            # Si no hay imagen, mostrar emoji
            image_label.setText("👋")
            image_label.setFont(QFont("Arial", 60))
            image_label.setStyleSheet(image_label.styleSheet() + "color: #4CAF50;")
        
        # Descripción
        desc_label = QLabel(self.word_data["description"])
        desc_label.setFont(QFont("Comic Sans MS", 11))
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet("""
            QLabel {
                color: #2E7D32;
                background: rgba(255, 255, 255, 0.3);
                border-radius: 8px;
                padding: 6px;
                margin: 2px;
            }
        """)
        
        # Agregar elementos al layout
        layout.addWidget(word_label)
        layout.addWidget(image_label)
        layout.addWidget(desc_label)
        
        self.setLayout(layout)
        self.setFixedSize(200, 300)

def create_section_header(title, subtitle, icon, colors):
    """Crear encabezado de sección"""
    container = QWidget()
    layout = QVBoxLayout()
    layout.setSpacing(10)
    layout.setContentsMargins(20, 20, 20, 20)
    
    # Título principal
    title_label = GradientTitleLabel(f"{icon} {title} {icon}", colors)
    title_label.setFont(QFont("Comic Sans MS", 26, QFont.Bold))
    title_label.setAlignment(Qt.AlignCenter)
    title_label.setMinimumHeight(70)
    title_label.setStyleSheet("border-radius: 15px; margin: 10px;")
    
    # Subtítulo
    subtitle_label = QLabel(subtitle)
    subtitle_label.setFont(QFont("Comic Sans MS", 16))
    subtitle_label.setAlignment(Qt.AlignCenter)
    subtitle_label.setWordWrap(True)
    subtitle_label.setStyleSheet(f"""
        QLabel {{
            color: #{colors[1][0]:02x}{colors[1][1]:02x}{colors[1][2]:02x};
            background: rgba(255, 255, 255, 0.7);
            border-radius: 12px;
            padding: 15px;
            margin: 10px;
            border: 2px solid rgba({colors[0][0]}, {colors[0][1]}, {colors[0][2]}, 0.3);
        }}
    """)
    
    layout.addWidget(title_label)
    layout.addWidget(subtitle_label)
    container.setLayout(layout)
    
    return container

def page_letters():
    """Página principal de aprendizaje mejorada"""
    
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
    
    # === TÍTULO PRINCIPAL ===
    main_title = GradientTitleLabel(
        "🎓 ¡Aprende el Lenguaje de Señas! 🎓", 
        [(255, 107, 157), (156, 39, 176), (33, 150, 243), (76, 175, 80)]
    )
    main_title.setFont(QFont("Comic Sans MS", 32, QFont.Bold))
    main_title.setAlignment(Qt.AlignCenter)
    main_title.setMinimumHeight(80)
    main_title.setStyleSheet("border-radius: 20px; margin: 20px;")
    
    # === SECCIÓN 1: ABECEDARIO ===
    letters_header = create_section_header(
        "Abecedario en Señas",
        "🔤 Aprende cada letra del abecedario con imágenes claras y divertidas. ¡Domina las bases del lenguaje de señas!",
        "📚",
        [(156, 39, 176), (74, 20, 140)]
    )
    
    # Grid de letras
    letters_container = QWidget()
    letters_grid = QGridLayout()
    letters_grid.setSpacing(15)
    letters_grid.setAlignment(Qt.AlignCenter)
    
    for i, letter in enumerate(list_letters):
        card = LetterCard(letter)
        row = i // 6
        col = i % 6
        letters_grid.addWidget(card, row, col)
    
    letters_container.setLayout(letters_grid)
    
    # === SECCIÓN 2: PALABRAS BÁSICAS ===
    words_header = create_section_header(
        "Palabras Básicas",
        "💬 Descubre palabras esenciales para comunicarte en el día a día. ¡Expande tu vocabulario en señas!",
        "🌟",
        [(76, 175, 80), (46, 125, 50)]
    )
    
    # Grid de palabras
    words_container = QWidget()
    words_grid = QGridLayout()
    words_grid.setSpacing(15)
    words_grid.setAlignment(Qt.AlignCenter)
    
    for i, word_data in enumerate(basic_words):
        card = WordCard(word_data)
        row = i // 4
        col = i % 4
        words_grid.addWidget(card, row, col)
    
    words_container.setLayout(words_grid)
    
    # === MENSAJE MOTIVACIONAL ===
    motivational_msg = QLabel("🌈 ¡Cada letra y palabra que aprendes te acerca más a una comunicación perfecta! 🌈")
    motivational_msg.setAlignment(Qt.AlignCenter)
    motivational_msg.setFont(QFont("Comic Sans MS", 18, QFont.Bold))
    motivational_msg.setStyleSheet("""
        QLabel {
            color: #FF6B9D;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 rgba(255, 255, 255, 0.8), 
                stop:1 rgba(248, 250, 255, 0.6));
            border-radius: 20px;
            padding: 20px;
            margin: 30px;
            border: 3px dashed #FF6B9D;
        }
    """)
    
    # === ENSAMBLAR TODO ===
    main_layout.addWidget(main_title)
    main_layout.addWidget(letters_header)
    main_layout.addWidget(letters_container)
    main_layout.addWidget(words_header)
    main_layout.addWidget(words_container)
    main_layout.addWidget(motivational_msg)
    main_layout.addStretch()
    
    content_widget.setLayout(main_layout)
    scroll_area.setWidget(content_widget)
    
    return scroll_area