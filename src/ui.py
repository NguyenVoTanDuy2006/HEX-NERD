from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QPushButton
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtCore import Qt, QSize, pyqtSignal
import config


def get_style_sheet(bg_color=config.COLOR_DEFAULT_BG, 
                    border_color=config.COLOR_BORDER_EMPTY, 
                    text_color=config.COLOR_DEFAULT_FG, 
                    bold=False):
    style = f"""
        background-color: {bg_color};
        border: 2px solid {border_color};
        color: {text_color};
    """
    if bold:
        style += "font-weight: bold;"
    
    return style

class ClickableLabel(QLabel):
    clicked = pyqtSignal(int)
    def __init__(self, index, parent=None):
        super().__init__(parent)
        self.index = index
        self.setCursor(Qt.CursorShape.PointingHandCursor)
    def mousePressEvent(self, event):
        self.clicked.emit(self.index)

def create_grid(nrow, ncol, font, size, clickable=False, click_handler=None):
    grid_container = QWidget()
    grid_layout = QGridLayout(grid_container)
    grid_layout.setSpacing(10)
    grid_labels = []
    for row in range(nrow):
        row_labels = []
        for col in range(ncol):
            if clickable:
                label = ClickableLabel(index=col)
                if click_handler: label.clicked.connect(click_handler)
            else: label = QLabel("")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter); label.setFont(font); label.setFixedSize(size, size)
            label.setStyleSheet(f"""
                border: 2px solid {config.COLOR_BORDER_EMPTY}; 
                color: {config.COLOR_DEFAULT_FG}; 
                background-color: {config.COLOR_DEFAULT_BG}; 
                font-weight: bold;
            """)
            grid_layout.addWidget(label, row, col); row_labels.append(label)
        grid_labels.append(row_labels)
    return grid_container, grid_labels

class SquareWidget(QWidget):
    def __init__(self, color, parent=None):
        super().__init__(parent)
        self._color = QColor(color)
    def paintEvent(self, event):
        painter = QPainter(self); painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(self._color); painter.setPen(Qt.PenStyle.NoPen); painter.drawRect(self.rect())
    def sizeHint(self): return QSize(100, 100)
    def set_color(self, color): self._color = QColor(color); self.update()

def create_square(w, h, color):
    square = SquareWidget(color=color); square.setFixedSize(QSize(w, h)); return square

def create_notification_label(font, size):
    notification_label = QLabel(""); notification_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    notification_label.setFont(font); notification_label.setFixedHeight(size); return notification_label