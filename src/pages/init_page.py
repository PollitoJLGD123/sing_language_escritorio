from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QTextEdit, 
    QPushButton, QFrame, QSpacerItem, QSizePolicy, QScrollArea
)
from PyQt5.QtGui import (
    QFont, QPalette, QLinearGradient, QBrush, QPainter, 
    QColor, QPixmap, QPen
)
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, pyqtProperty

class GradientLabel(QLabel):
    """Label personalizado con gradiente de fondo mejorado"""
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.gradient_colors = [(138, 43, 226), (30, 144, 255), (50, 205, 50)]
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Crear gradiente
        gradient = QLinearGradient(0, 0, self.width(), 0)
        gradient.setColorAt(0, QColor(*self.gradient_colors[0]))
        gradient.setColorAt(0.5, QColor(*self.gradient_colors[1]))
        gradient.setColorAt(1, QColor(*self.gradient_colors[2]))
        
        # Dibujar fondo con gradiente
        painter.fillRect(self.rect(), QBrush(gradient))
        
        # Dibujar texto con sombra
        painter.setPen(QColor(0, 0, 0, 50))  # Sombra
        painter.drawText(self.rect().adjusted(2, 2, 2, 2), self.alignment(), self.text())
        
        painter.setPen(QColor(255, 255, 255))  # Texto principal
        painter.drawText(self.rect(), self.alignment(), self.text())

class AnimatedButton(QPushButton):
    """Botón con animaciones y efectos hover mejorados"""
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #FF6B9D, stop:0.5 #9C27B0, stop:1 #2196F3);
                color: white;
                border: none;
                border-radius: 30px;
                padding: 18px 40px;
                font-size: 20px;
                font-weight: bold;
                font-family: 'Comic Sans MS';
                box-shadow: 0 8px 16px rgba(156, 39, 176, 0.3);
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #FF5722, stop:0.5 #7B1FA2, stop:1 #1976D2);
                box-shadow: 0 12px 24px rgba(156, 39, 176, 0.4);
                transform: translateY(-2px);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #E91E63, stop:0.5 #6A1B9A, stop:1 #1565C0);
                transform: translateY(1px);
            }
        """)

class ImprovedFeatureCard(QFrame):
    """Tarjeta de característica mejorada con mejor tamaño y diseño"""
    def __init__(self, icon, title, description, color_scheme, parent=None):
        super().__init__(parent)
        self.setupUI(icon, title, description, color_scheme)
        
    def setupUI(self, icon, title, description, color_scheme):
        # Configurar el frame principal
        self.setFrameStyle(QFrame.NoFrame)
        self.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {color_scheme['light']}, stop:1 {color_scheme['lighter']});
                border: 3px solid {color_scheme['border']};
                border-radius: 20px;
                margin: 15px;
                padding: 0px;
            }}
            QFrame:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {color_scheme['lighter']}, stop:1 {color_scheme['light']});
                border: 3px solid {color_scheme['main']};
                transform: translateY(-5px);
                box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
            }}
        """)
        
        # Layout principal con más espacio
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 40, 30, 40)
        
        # Contenedor del icono con mejor diseño
        icon_container = QFrame()
        icon_container.setFixedSize(80, 80)
        icon_container.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {color_scheme['main']}, stop:1 {color_scheme['dark']});
                border-radius: 40px;
                border: 3px solid rgba(255, 255, 255, 0.3);
            }}
        """)
        
        icon_layout = QVBoxLayout()
        icon_layout.setContentsMargins(0, 0, 0, 0)
        
        # Icono
        icon_label = QLabel(icon)
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setFont(QFont("Arial", 32))
        icon_label.setStyleSheet("color: white; background: transparent; border: none;")
        
        icon_layout.addWidget(icon_label)
        icon_container.setLayout(icon_layout)
        
        # Título con mejor tipografía
        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Comic Sans MS", 18, QFont.Bold))
        title_label.setStyleSheet(f"""
            color: {color_scheme['dark']}; 
            margin: 15px 0px 10px 0px;
            padding: 5px;
            background: transparent;
        """)
        title_label.setWordWrap(True)
        
        # Descripción con mejor formato
        desc_label = QLabel(description)
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setWordWrap(True)
        desc_label.setFont(QFont("Comic Sans MS", 14))
        desc_label.setStyleSheet(f"""
            color: {color_scheme['text']}; 
            line-height: 1.6;
            padding: 10px;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 10px;
            margin: 5px;
        """)
        
        # Agregar elementos al layout
        layout.addWidget(icon_container, 0, Qt.AlignCenter)
        layout.addWidget(title_label)
        layout.addWidget(desc_label)
        layout.addStretch()
        
        self.setLayout(layout)
        
        # Establecer tamaño mínimo más grande
        self.setMinimumSize(320, 400)
        self.setMaximumWidth(400)

def page_init():
    """Función principal que retorna el widget mejorado"""
    
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
                stop:0 #FFE5F1, stop:0.25 #E8F4FD, 
                stop:0.5 #F0F8E8, stop:0.75 #FFF0E6, stop:1 #F5E6FF);
            font-family: 'Comic Sans MS';
        }
    """)
    
    # Layout principal
    main_layout = QVBoxLayout()
    main_layout.setSpacing(40)
    main_layout.setContentsMargins(50, 50, 50, 50)
    
    # === SECCIÓN HERO MEJORADA ===
    hero_layout = QVBoxLayout()
    hero_layout.setAlignment(Qt.AlignCenter)
    hero_layout.setSpacing(25)
    
    # Badge mejorado
    badge = QLabel("✨ ¡Aprende jugando con diversión! ✨")
    badge.setAlignment(Qt.AlignCenter)
    badge.setFont(QFont("Comic Sans MS", 14, QFont.Bold))
    badge.setStyleSheet("""
        QLabel {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #FFB74D, stop:0.5 #E1BEE7, stop:1 #81C784);
            color: #4A148C;
            border-radius: 25px;
            padding: 12px 24px;
            margin: 10px;
            border: 2px solid rgba(255, 255, 255, 0.5);
        }
    """)
    
    # Título principal mejorado
    titulo = GradientLabel("🌟 Descubre el Maravilloso Mundo de las Señas 🌟")
    titulo.setFont(QFont("Comic Sans MS", 32, QFont.Bold))
    titulo.setAlignment(Qt.AlignCenter)
    titulo.setMinimumHeight(100)
    titulo.setStyleSheet("border-radius: 20px; margin: 15px; padding: 10px;")
    
    # Descripción mejorada
    descripcion = QLabel(
        "🚀 ¡Embárcate en una aventura increíble para aprender el abecedario y palabras básicas "
        "en lenguaje de señas! Practica con tu cámara, juega y mejora cada día. "
        "¡La diversión y el aprendizaje van de la mano! 🎉"
    )
    descripcion.setFont(QFont("Comic Sans MS", 18))
    descripcion.setAlignment(Qt.AlignCenter)
    descripcion.setWordWrap(True)
    descripcion.setStyleSheet("""
        QLabel {
            color: #2E2E2E;
            line-height: 1.8;
            margin: 25px;
            padding: 30px;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 rgba(255, 255, 255, 0.9), 
                stop:1 rgba(248, 250, 255, 0.8));
            border-radius: 20px;
            border: 2px solid rgba(156, 39, 176, 0.2);
        }
    """)
    descripcion.setMinimumHeight(200)
    
    # Botón principal mejorado
    start_button = AnimatedButton("💖 ¡Comenzar Mi Aventura de Aprendizaje! 💖")
    start_button.setMinimumHeight(70)
    start_button.setMaximumWidth(450)
    
    # Agregar elementos al hero
    hero_layout.addWidget(badge)
    hero_layout.addWidget(titulo)
    hero_layout.addWidget(descripcion)
    hero_layout.addWidget(start_button)
    
    # === TÍTULO DE SECCIÓN ===
    section_title = QLabel("🎯 ¿Qué puedes hacer en nuestra aplicación? 🎯")
    section_title.setAlignment(Qt.AlignCenter)
    section_title.setFont(QFont("Comic Sans MS", 24, QFont.Bold))
    section_title.setStyleSheet("""
        QLabel {
            color: #4A148C;
            margin: 30px 0px 20px 0px;
            padding: 15px;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 rgba(255, 193, 7, 0.3), 
                stop:0.5 rgba(156, 39, 176, 0.2), 
                stop:1 rgba(76, 175, 80, 0.3));
            border-radius: 15px;
            border: 2px solid rgba(156, 39, 176, 0.3);
        }
    """)
    
    # === SECCIÓN DE TARJETAS MEJORADAS ===
    cards_container = QWidget()
    cards_layout = QHBoxLayout()
    cards_layout.setSpacing(30)
    cards_layout.setAlignment(Qt.AlignCenter)
    
    # Esquemas de colores mejorados
    color_schemes = [
        {
            'main': '#9C27B0', 'dark': '#6A1B9A', 'light': '#F3E5F5', 
            'lighter': '#FCE4EC', 'border': '#E1BEE7', 'text': '#4A148C'
        },
        {
            'main': '#2196F3', 'dark': '#1565C0', 'light': '#E3F2FD', 
            'lighter': '#F0F8FF', 'border': '#BBDEFB', 'text': '#0D47A1'
        },
        {
            'main': '#4CAF50', 'dark': '#2E7D32', 'light': '#E8F5E8', 
            'lighter': '#F1F8E9', 'border': '#C8E6C9', 'text': '#1B5E20'
        }
    ]
    
    # Datos de las tarjetas mejorados
    cards_data = [
        ("📚", "Aprende el Abecedario", 
         "Descubre cada letra del abecedario con ilustraciones súper claras, divertidas y fáciles de entender. ¡Cada letra es una nueva aventura!", 
         color_schemes[0]),
        ("📹", "Practica con tu Cámara", 
         "Usa tu cámara web para practicar en tiempo real y recibir retroalimentación instantánea. ¡Verás tu progreso al instante!", 
         color_schemes[1]),
        ("🔍", "Busca Cualquier Palabra", 
         "Encuentra cómo hacer cualquier palabra en lenguaje de señas con nuestro buscador inteligente. ¡Explora sin límites!", 
         color_schemes[2])
    ]
    
    # Crear tarjetas mejoradas
    for icon, title, desc, colors in cards_data:
        card = ImprovedFeatureCard(icon, title, desc, colors)
        cards_layout.addWidget(card)
    
    cards_container.setLayout(cards_layout)
    
    # === ELEMENTOS DECORATIVOS MEJORADOS ===
    decorative_container = QWidget()
    decorative_layout = QVBoxLayout()
    
    # Mensaje motivacional
    motivational_msg = QLabel("🌈 ¡Cada día es una oportunidad para aprender algo nuevo! 🌈")
    motivational_msg.setAlignment(Qt.AlignCenter)
    motivational_msg.setFont(QFont("Comic Sans MS", 16, QFont.Bold))
    motivational_msg.setStyleSheet("""
        QLabel {
            color: #FF6B9D;
            margin: 20px;
            padding: 15px;
            background: rgba(255, 255, 255, 0.6);
            border-radius: 15px;
            border: 2px dashed #FF6B9D;
        }
    """)
    
    # Estrellas animadas
    stars_layout = QHBoxLayout()
    stars_layout.setAlignment(Qt.AlignCenter)
    
    star_colors = ["#FFD700", "#FF6B9D", "#9C27B0", "#2196F3", "#4CAF50"]
    for i in range(5):
        star = QLabel("⭐")
        star.setFont(QFont("Arial", 28))
        star.setAlignment(Qt.AlignCenter)
        star.setStyleSheet(f"""
            color: {star_colors[i]}; 
            margin: 8px;
            padding: 5px;
            background: rgba(255, 255, 255, 0.3);
            border-radius: 20px;
        """)
        stars_layout.addWidget(star)
    
    decorative_layout.addWidget(motivational_msg)
    decorative_layout.addLayout(stars_layout)
    decorative_container.setLayout(decorative_layout)
    
    # === ENSAMBLAR TODO ===
    main_layout.addLayout(hero_layout)
    main_layout.addWidget(section_title)
    main_layout.addWidget(cards_container)
    main_layout.addWidget(decorative_container)
    main_layout.addStretch()
    
    content_widget.setLayout(main_layout)
    scroll_area.setWidget(content_widget)
    
    return scroll_area