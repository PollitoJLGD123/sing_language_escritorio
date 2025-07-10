from PyQt5.QtWidgets import (
    QMainWindow,
    QTabWidget
)
from PyQt5.QtGui import QFont
from src.pages.init_page import page_init
from src.pages.learn_page import page_letters
from src.pages.practice_page import page_practice
from src.pages.search_page import page_search

def create_tabs():
    tabs = QTabWidget()
    tabs.setFont(QFont("Comic Sans MS", 12))
    tabs.setTabPosition(QTabWidget.North)

    tabs.addTab(page_init(), "Inicio")
    tabs.addTab(page_letters(), "Aprender")
    tabs.addTab(page_practice(), "Practicar")
    tabs.addTab(page_search(), "Buscar")

    return tabs