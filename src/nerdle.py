from collections import Counter

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, QTimer, pyqtSignal

import config
import ui
from nerdle_logic import NerdleLogic

class NerdleMinigame(QWidget):
    game_won_signal = pyqtSignal(str)
    back_to_main_signal = pyqtSignal()
    game_given_up_signal = pyqtSignal()
    game_lost_signal = pyqtSignal()

    # --- Initialization and UI Setup ---
    def __init__(self):
        super().__init__()
        self.logic = NerdleLogic()
        self.hex_char_to_reveal = ""
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter) 
        layout.setSpacing(15)
        
        title = QLabel("Find the two numbers for the equation")
        title.setFont(QFont("Arial", 20))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        guess_rows_container = QWidget()
        guess_rows_layout = QVBoxLayout(guess_rows_container)
        guess_rows_layout.setSpacing(10) 
        self.guess_rows = []
        font = QFont("Arial", 24, QFont.Weight.Bold)
        for _ in range(6):
            row_widget = QWidget()
            row_layout = QHBoxLayout(row_widget)
            row_layout.setSpacing(10)
            row_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            n1_labels = [self._create_input_label(font) for _ in range(2)]
            operator_label = QLabel("+")
            operator_label.setFont(font)
            
            n2_labels = [self._create_input_label(font) for _ in range(2)]
            result_label = QLabel("= ??")
            result_label.setFont(font)
            
            for label in n1_labels: row_layout.addWidget(label)
            row_layout.addWidget(operator_label)
            
            for label in n2_labels: row_layout.addWidget(label)
            row_layout.addWidget(result_label); guess_rows_layout.addWidget(row_widget)
            self.guess_rows.append({"widget": row_widget, "inputs": n1_labels + n2_labels, "operator": operator_label, "result": result_label})
        layout.addWidget(guess_rows_container)
        
        self.notification_label = ui.create_notification_label(QFont("Arial", 14), 30)
        self.notification_timer = QTimer(self); self.notification_timer.setSingleShot(True); self.notification_timer.setInterval(2500)
        self.notification_timer.timeout.connect(lambda: self.notification_label.setText(""))
        layout.addWidget(self.notification_label)
        
        
        give_up_button = QPushButton("Give up"); give_up_button.clicked.connect(self.game_given_up_signal.emit)
        layout.addWidget(give_up_button, alignment=Qt.AlignmentFlag.AlignCenter)

    def start_new_minigame(self, hex_char):
        self.logic.start_new_minigame()
        self.hex_char_to_reveal = hex_char

        for i, row in enumerate(self.guess_rows):
            for label in row["inputs"]: 
                label.setText("")
                label.setStyleSheet(ui.get_style_sheet())
            row["operator"].setText(self.logic.operator)
            row["result"].setText(f"= {self.logic.result}")
            row["widget"].setVisible(i == 0)
        self.show_notification("New problem! Fill in the blanks.")

    def keyPressEvent(self, event):
        if self.logic.is_game_over: return
        key = event.text()
        if event.key() == Qt.Key.Key_Backspace: self.logic.handle_key_press("BACKSPACE")
        elif key in "0123456789" and len(key) == 1: self.logic.handle_key_press(key)
        elif event.key() in [Qt.Key.Key_Return, Qt.Key.Key_Enter]: self.submit_guess()
        self._update_display()

    def submit_guess(self):
        result = self.logic.submit_guess()
        if result['status'] == "invalid":
            self.show_notification(result['message']); return
        current_row_idx = self.logic.current_row - 1 
        current_input_labels = self.guess_rows[current_row_idx]["inputs"]
        color_map = {
            "correct_place": config.COLOR_CORRECT_PLACE,
            "correct_letter": config.COLOR_CORRECT_LETTER,
            "wrong_letter": config.COLOR_WRONG_LETTER
        }
        for i, color_key in enumerate(result['colors']):
            color_val = color_map[color_key]
            current_input_labels[i].setStyleSheet(ui.get_style_sheet(bg_color=color_val, border_color=color_val, bold=True))

        if result['status'] == 'win':
            self.show_notification("You won!")
            self.game_won_signal.emit(self.hex_char_to_reveal)
            QTimer.singleShot(1500, self.back_to_main_signal.emit)
        elif result['status'] == 'lose':
            self.show_notification(f"You lost! Answer: {self.logic.secret_n1} {self.logic.operator} {self.logic.secret_n2}")
            QTimer.singleShot(2000, self.game_lost_signal.emit)
        else: # continue
            self.guess_rows[self.logic.current_row]["widget"].setVisible(True)
            self.show_notification(result['message'])

    def _update_display(self):
        for r_idx, row_data in enumerate(self.logic.guesses):
            for c_idx, char in enumerate(row_data):
                label = self.guess_rows[r_idx]["inputs"][c_idx]
                label.setText(char)

    def _create_input_label(self, font):
        label = QLabel(""); label.setFont(font); label.setFixedSize(50, 50); label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet(ui.get_style_sheet())
        return label

    def show_notification(self, message):
        self.notification_label.setText(message)
        self.notification_timer.start()