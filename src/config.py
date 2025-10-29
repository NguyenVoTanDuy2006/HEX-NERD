COLOR_DEFAULT_BG = "#2c2c2c"  
COLOR_DEFAULT_FG = "#ffffff"  

# Màu cho các ô đoán
COLOR_CORRECT_PLACE = "#6aaa64"   
COLOR_CORRECT_LETTER = "#c9b458"  
COLOR_WRONG_LETTER = "#4a4a4a"    
COLOR_GIVE_UP = "#d9534f"         

# Màu cho các đường viền
COLOR_BORDER_EMPTY = "#555555" 
COLOR_BORDER_FILLED = "#666666" 

# Màu cho nút bấm
COLOR_BUTTON_BG = "#555555"
COLOR_BUTTON_HOVER_BG = "#6a6a6a"

STYLESHEET = f"""
    QMainWindow, QWidget {{
        background-color: {COLOR_DEFAULT_BG};
    }}
    QLabel {{
        color: {COLOR_DEFAULT_FG};
    }}
    QPushButton {{
        background-color: {COLOR_BUTTON_BG};
        color: {COLOR_DEFAULT_FG};
        font-size: 16px;
        font-weight: bold;
        border: none;
        padding: 10px;
        border-radius: 5px;
    }}
    QPushButton:hover {{
        background-color: {COLOR_BUTTON_HOVER_BG};
    }}
    QMessageBox {{
        background-color: {COLOR_DEFAULT_BG};
    }}
    QMessageBox QLabel {{
        color: {COLOR_DEFAULT_FG};
    }}
"""