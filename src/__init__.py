from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt
from src.components.tabs import create_tabs

def create_app():
    """Create the main application with a modern design.
    
    This function initializes a QMainWindow with a frameless and maximized window state,
    sets a fixed minimum size, and applies a gradient background style. It creates a 
    central widget with a QVBoxLayout, adds an enhanced tabs widget, and sets it as 
    the central widget of the main window.
    """
    app = QMainWindow()
    
    # Configuración básica de la ventana
    app.setWindowTitle("🌟 Lenguaje de Señas para Niños - Aprende Jugando 🌟")
    app.setWindowFlags(Qt.Window)  # Sin bordes
    app.setWindowState(Qt.WindowMaximized)  # Maximizado
    app.setMinimumSize(1920, 1080)  # Tamaño fijo
    
    # Crear widget central con layout
    central_widget = QWidget()
    central_layout = QVBoxLayout()
    central_layout.setContentsMargins(0, 0, 0, 0)  # Sin márgenes
    central_layout.setSpacing(0)
    
    # Aplicar estilo principal con gradiente de fondo
    app.setStyleSheet("""
        QMainWindow {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #FFD7E9, stop:0.33 #E8F5E9, 
                stop:0.66 #E3F2FD, stop:1 #FFE5F1);
            border: none;
        }
        
        QWidget {
            background: transparent;
            font-family: 'Comic Sans MS', cursive;
        }
        
        QTabWidget::pane {
            background: transparent;
        }
        
        QTabBar::tab {
            background: rgba(255, 255, 255, 0.9);
            border: none;
            padding: 10px 20px;
            margin-right: 5px;
            border-radius: 15px;
        }
        
        QTabBar::tab:selected {
            background: rgba(255, 255, 255, 0.95);
        }
    """)
    
    # Crear y agregar las tabs mejoradas
    tabs_widget = create_tabs()
    central_layout.addWidget(tabs_widget)
    
    central_widget.setLayout(central_layout)
    app.setCentralWidget(central_widget)
    
    return app