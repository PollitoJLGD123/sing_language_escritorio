from src import create_app
import sys
from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = create_app()
    window.show()
    sys.exit(app.exec_())
