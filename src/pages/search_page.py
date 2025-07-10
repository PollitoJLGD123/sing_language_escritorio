from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit,
    QPushButton, QFrame, QGridLayout, QScrollArea, QSpacerItem, QSizePolicy
)
from PyQt5.QtGui import QFont, QPixmap, QPainter, QLinearGradient, QBrush, QColor, QMovie
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal
import time

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

class SearchThread(QThread):
    """Hilo para simular búsqueda asíncrona"""
    search_completed = pyqtSignal(list)
    
    def __init__(self, search_term):
        super().__init__()
        self.search_term = search_term
    
    def run(self):
        # Simular tiempo de búsqueda
        time.sleep(1)
        # Dividir la palabra en letras
        letters = [letter.upper() for letter in self.search_term if letter.isalpha()]
        self.search_completed.emit(letters)

class StyledButton(QPushButton):
    """Botón personalizado con estilos"""
    def __init__(self, text="", button_type="primary", parent=None):
        super().__init__(text, parent)
        self.setFont(QFont("Comic Sans MS", 12, QFont.Bold))
        self.setMinimumHeight(45)
        
        if button_type == "primary":
            self.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #9C27B0, stop:1 #2196F3);
                    color: white;
                    border: none;
                    border-radius: 22px;
                    padding: 12px 24px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #7B1FA2, stop:1 #1976D2);
                    transform: translateY(-2px);
                }
                QPushButton:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #6A1B9A, stop:1 #1565C0);
                }
                QPushButton:disabled {
                    background: #CCCCCC;
                    color: #666666;
                }
            """)
        elif button_type == "popular":
            self.setStyleSheet("""
                QPushButton {
                    background: rgba(255, 255, 255, 0.9);
                    color: #9C27B0;
                    border: 2px solid #E1BEE7;
                    border-radius: 15px;
                    padding: 10px 20px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background: rgba(156, 39, 176, 0.1);
                    border: 2px solid #9C27B0;
                    transform: scale(1.05);
                }
                QPushButton:pressed {
                    background: rgba(156, 39, 176, 0.2);
                }
            """)

class LetterCard(QFrame):
    """Tarjeta para mostrar una letra individual"""
    def __init__(self, letter, position, parent=None):
        super().__init__(parent)
        self.letter = letter
        self.position = position
        self.setupUI()
        
    def setupUI(self):
        self.setFrameStyle(QFrame.NoFrame)
        self.setFixedSize(160, 200)
        self.setStyleSheet("""
            QFrame {
                background: rgba(255, 255, 255, 0.95);
                border-radius: 15px;
                border: 2px solid rgba(76, 175, 80, 0.3);
                margin: 8px;
            }
            QFrame:hover {
                background: rgba(255, 255, 255, 1.0);
                border: 2px solid #4CAF50;
                transform: scale(1.05);
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setAlignment(Qt.AlignCenter)
        
        # Badge de posición
        position_badge = QLabel(f"Letra {self.position}")
        position_badge.setFont(QFont("Comic Sans MS", 10, QFont.Bold))
        position_badge.setAlignment(Qt.AlignCenter)
        position_badge.setStyleSheet("""
            QLabel {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4CAF50, stop:1 #2196F3);
                color: white;
                border-radius: 10px;
                padding: 4px 8px;
                margin: 2px;
            }
        """)
        
        # Letra grande
        letter_label = QLabel(self.letter)
        letter_label.setFont(QFont("Comic Sans MS", 24, QFont.Bold))
        letter_label.setAlignment(Qt.AlignCenter)
        letter_label.setStyleSheet("""
            QLabel {
                color: #2E7D32;
                background: rgba(76, 175, 80, 0.1);
                border-radius: 8px;
                padding: 8px;
                margin: 4px;
            }
        """)
        
        # Imagen de la letra
        image_label = QLabel()
        image_label.setAlignment(Qt.AlignCenter)
        image_label.setFixedSize(80, 80)
        image_label.setStyleSheet("""
            QLabel {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(156, 39, 176, 0.1), 
                    stop:1 rgba(33, 150, 243, 0.1));
                border-radius: 10px;
                border: 2px solid rgba(76, 175, 80, 0.2);
                padding: 5px;
            }
        """)
        
        image_label.setFixedSize(150, 150)
        
        # Cargar imagen
        pixmap = QPixmap(f"images/utils/{self.letter.lower()}.jpg")
        if not pixmap.isNull():
            pixmap = pixmap.scaled(130, 130, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            image_label.setPixmap(pixmap)
        else:
            # Fallback a emoji
            image_label.setText("🤟")
            image_label.setFont(QFont("Arial", 30))
            image_label.setStyleSheet(image_label.styleSheet() + "color: #4CAF50;")
        
        layout.addWidget(position_badge)
        layout.addWidget(letter_label)
        layout.addWidget(image_label)
        
        self.setLayout(layout)
        self.setFixedSize(250, 350)

class SearchCard(QFrame):
    """Tarjeta para el área de búsqueda"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUI()
        
    def setupUI(self):
        self.setFrameStyle(QFrame.NoFrame)
        self.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(33, 150, 243, 0.1), 
                    stop:1 rgba(156, 39, 176, 0.05));
                border: 3px solid #BBDEFB;
                border-radius: 20px;
                padding: 10px;
                margin: 15px;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Campo de búsqueda y botón
        search_layout = QHBoxLayout()
        search_layout.setSpacing(15)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Escribe una palabra... (ej: HOLA, MAMÁ, GRACIAS)")
        self.search_input.setFont(QFont("Comic Sans MS", 14))
        self.search_input.setMinimumHeight(50)
        self.search_input.setStyleSheet("""
            QLineEdit {
                background: rgba(255, 255, 255, 0.9);
                border: 2px solid #E1BEE7;
                border-radius: 25px;
                padding: 12px 20px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #9C27B0;
                background: rgba(255, 255, 255, 1.0);
            }
        """)
        
        self.search_button = StyledButton("🔍 Buscar", "primary")
        self.search_button.setMinimumWidth(120)
        
        # Indicador de carga
        self.loading_label = QLabel()
        self.loading_label.setAlignment(Qt.AlignCenter)
        self.loading_label.setFont(QFont("Comic Sans MS", 12))
        self.loading_label.setStyleSheet("color: #666666;")
        self.loading_label.hide()
        
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_button)
        
        layout.addLayout(search_layout)
        layout.addWidget(self.loading_label)
        
        self.setLayout(layout)

class ResultsCard(QFrame):
    """Tarjeta para mostrar resultados de búsqueda"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUI()
        
    def setupUI(self):
        self.setFrameStyle(QFrame.NoFrame)
        self.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(76, 175, 80, 0.1), 
                    stop:1 rgba(33, 150, 243, 0.05));
                border: 3px solid #C8E6C9;
                border-radius: 20px;
                padding: 10px;
                margin: 15px;
            }
        """)
        
        self.layout = QVBoxLayout()
        self.layout.setSpacing(20)
        self.layout.setContentsMargins(30, 30, 30, 30)
        
        # Título de resultados
        self.title_label = QLabel()
        self.title_label.setFont(QFont("Comic Sans MS", 20, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("""
            QLabel {
                color: #2E7D32;
                background: rgba(255, 255, 255, 0.7);
                border-radius: 15px;
                padding: 15px;
                margin: 10px;
            }
        """)
        
        # Área de scroll para las letras
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setStyleSheet("""
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
                    stop:0 #4CAF50, stop:1 #2196F3);
                border-radius: 6px;
                min-height: 20px;
            }
        """)
        
        self.letters_widget = QWidget()
        self.letters_layout = QGridLayout()
        self.letters_layout.setSpacing(15)
        self.letters_layout.setAlignment(Qt.AlignCenter)
        self.letters_widget.setLayout(self.letters_layout)
        self.scroll_area.setWidget(self.letters_widget)
        
        # Instrucción
        self.instruction_label = QLabel()
        self.instruction_label.setFont(QFont("Comic Sans MS", 14))
        self.instruction_label.setAlignment(Qt.AlignCenter)
        self.instruction_label.setWordWrap(True)
        self.instruction_label.setStyleSheet("""
            QLabel {
                color: #424242;
                background: rgba(255, 255, 255, 0.8);
                border-radius: 12px;
                padding: 15px;
                margin: 10px;
                border: 2px solid rgba(76, 175, 80, 0.2);
            }
        """)
        
        self.layout.addWidget(self.title_label)
        self.layout.addWidget(self.scroll_area)
        self.layout.addWidget(self.instruction_label)
        
        self.setLayout(self.layout)
        self.hide()  # Inicialmente oculto
    
    def show_results(self, word, letters):
        """Mostrar resultados de búsqueda"""
        # Limpiar layout anterior
        for i in reversed(range(self.letters_layout.count())):
            self.letters_layout.itemAt(i).widget().setParent(None)
        
        # Actualizar título
        self.title_label.setText(f'✨ Señas para "{word.upper()}" ✨')
        
        # Agregar tarjetas de letras
        for i, letter in enumerate(letters):
            card = LetterCard(letter, i + 1)
            row = i // 6
            col = i % 6
            self.letters_layout.addWidget(card, row, col)
        
        # Actualizar instrucción
        self.instruction_label.setText(
            f'📖 Para formar la palabra "{word.upper()}", haz las señas de cada letra en orden'
        )
        
        self.show()

class PopularWordsCard(QFrame):
    """Tarjeta para palabras populares"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.popular_words = ["HOLA", "GRACIAS", "MAMÁ", "PAPÁ", "AGUA", "CASA", "AMOR", "FELIZ"]
        self.setupUI()
        
    def setupUI(self):
        self.setFrameStyle(QFrame.NoFrame)
        self.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(156, 39, 176, 0.1), 
                    stop:1 rgba(233, 30, 99, 0.05));
                border: 3px solid #E1BEE7;
                border-radius: 20px;
                padding: 10px;
                margin: 15px;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Título
        title = QLabel("🌟 Palabras Populares 🌟")
        title.setFont(QFont("Comic Sans MS", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                color: #7B1FA2;
                background: rgba(255, 255, 255, 0.7);
                border-radius: 15px;
                padding: 15px;
                margin: 10px;
            }
        """)
        
        # Subtítulo
        subtitle = QLabel("Haz clic en cualquier palabra para ver sus señas")
        subtitle.setFont(QFont("Comic Sans MS", 14))
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("""
            QLabel {
                color: #424242;
                background: rgba(255, 255, 255, 0.5);
                border-radius: 10px;
                padding: 10px;
                margin: 5px;
            }
        """)
        
        # Grid de botones
        buttons_widget = QWidget()
        buttons_layout = QGridLayout()
        buttons_layout.setSpacing(15)
        buttons_layout.setAlignment(Qt.AlignCenter)
        
        self.word_buttons = []
        for i, word in enumerate(self.popular_words):
            button = StyledButton(word, "popular")
            button.setMinimumHeight(50)
            self.word_buttons.append(button)
            row = i // 4
            col = i % 4
            buttons_layout.addWidget(button, row, col)
        
        buttons_widget.setLayout(buttons_layout)
        
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(buttons_widget)
        
        self.setLayout(layout)

def page_search():
    """Página principal de búsqueda"""
    
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
    title = GradientLabel("🔍 Buscador de Señas 🔍", [(138, 43, 226), (33, 150, 243)])
    title.setFont(QFont("Comic Sans MS", 32, QFont.Bold))
    title.setAlignment(Qt.AlignCenter)
    title.setMinimumHeight(80)
    title.setStyleSheet("border-radius: 20px; margin: 10px;")
    
    # Subtítulo
    subtitle = QLabel("Escribe cualquier palabra y descubre cómo hacerla en lenguaje de señas")
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
    
    # === COMPONENTES PRINCIPALES ===
    search_card = SearchCard()
    results_card = ResultsCard()
    popular_card = PopularWordsCard()
    
    # === FUNCIONALIDAD ===
    search_thread = None
    
    def perform_search():
        nonlocal search_thread
        search_term = search_card.search_input.text().strip()
        
        if not search_term:
            return
        
        # Mostrar estado de carga
        search_card.search_button.setEnabled(False)
        search_card.search_button.setText("🔄 Buscando...")
        search_card.loading_label.setText("Procesando tu búsqueda...")
        search_card.loading_label.show()
        results_card.hide()
        
        # Iniciar búsqueda en hilo separado
        search_thread = SearchThread(search_term)
        search_thread.search_completed.connect(lambda letters: on_search_completed(search_term, letters))
        search_thread.start()
    
    def on_search_completed(word, letters):
        # Ocultar estado de carga
        search_card.search_button.setEnabled(True)
        search_card.search_button.setText("🔍 Buscar")
        search_card.loading_label.hide()
        
        # Mostrar resultados
        if letters:
            results_card.show_results(word, letters)
        else:
            results_card.hide()
    
    def search_popular_word(word):
        search_card.search_input.setText(word)
        perform_search()
    
    # === CONECTAR EVENTOS ===
    search_card.search_button.clicked.connect(perform_search)
    search_card.search_input.returnPressed.connect(perform_search)
    
    # Conectar botones de palabras populares
    for i, button in enumerate(popular_card.word_buttons):
        word = popular_card.popular_words[i]
        button.clicked.connect(lambda checked, w=word: search_popular_word(w))
    
    # === ENSAMBLAR TODO ===
    main_layout.addLayout(header_layout)
    main_layout.addWidget(search_card)
    main_layout.addWidget(results_card)
    main_layout.addWidget(popular_card)
    main_layout.addStretch()
    
    content_widget.setLayout(main_layout)
    scroll_area.setWidget(content_widget)
    
    return scroll_area