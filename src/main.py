import sys
from PyQt6.QtWidgets import QApplication
from hexle import run
import config

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(config.STYLESHEET)
    run()