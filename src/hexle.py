import sys
import random
from collections import Counter

from PyQt6.QtWidgets import (
    QMainWindow, QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QStackedWidget, QPushButton, QMessageBox
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

import config
import ui
from nerdle import NerdleMinigame
from hexle_logic import HexleGameLogic

WINDOW_TITLE = "Hexle - Color Guessing Game"

class HexleGame(QMainWindow):
    MAX_FINAL_GUESSES = 4

    # Initialization 
    def __init__(self):
        super().__init__()
        self.setWindowTitle(WINDOW_TITLE)
        self.setFixedSize(700, 800)

        self.logic = HexleGameLogic()
        self.current_clicked_index = -1

        self.setup_ui()
        self.start_new_game()

    def setup_ui(self):
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Main Game Widget
        self.main_game_widget = QWidget()
        main_layout = QVBoxLayout(self.main_game_widget)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.setSpacing(20)

        status_layout = QHBoxLayout()
        status_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hexle_grid, self.hexle_labels = ui.create_grid(1, 6, QFont("Arial", 24), 60, clickable=True, click_handler=self.on_cell_clicked)
        status_layout.addWidget(self.hexle_grid)
        self.color_ui = ui.create_square(60, 60, "#FFFFFF")
        status_layout.addWidget(self.color_ui)
        main_layout.addLayout(status_layout)

        final_guess_container, self.final_guess_labels = ui.create_grid(self.MAX_FINAL_GUESSES, 6, QFont("Arial", 24, QFont.Weight.Bold), 60)
        main_layout.addWidget(final_guess_container)

        self.main_notification_label = ui.create_notification_label(QFont("Arial", 16), 40)
        main_layout.addWidget(self.main_notification_label)
        
        give_up_button = QPushButton("Give Up")
        give_up_button.clicked.connect(self.handle_give_up)
        main_layout.addWidget(give_up_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # Nerdle Minigame Widget
        self.nerdle_minigame_widget = NerdleMinigame()
        self.nerdle_minigame_widget.game_won_signal.connect(self.on_minigame_won)
        self.nerdle_minigame_widget.back_to_main_signal.connect(self.show_main_game_screen)
        self.nerdle_minigame_widget.game_lost_signal.connect(self.on_minigame_cant_solve)
        self.nerdle_minigame_widget.game_given_up_signal.connect(self.on_minigame_cant_solve)
        
        self.stacked_widget.addWidget(self.main_game_widget)
        self.stacked_widget.addWidget(self.nerdle_minigame_widget)

    def start_new_game(self):
        self.logic.start_new_game()

        self.color_ui.set_color(f"#{self.logic.secret_color_code}")
        
        for label in self.hexle_labels[0]: 
            label.setText("?")
            label.setStyleSheet(ui.get_style_sheet(bold=True))
        
        for row in self.final_guess_labels:
            for label in row: 
                label.setText("")
                label.setStyleSheet(ui.get_style_sheet())
        
        self.main_notification_label.setText("Click a '?' to solve. Type your final guess below.")
        self.show_main_game_screen()

    def keyPressEvent(self, event):
        if self.stacked_widget.currentWidget() is not self.main_game_widget or self.logic.is_game_over: 
            return
        
        key = event.text().upper()
        
        if event.key() == Qt.Key.Key_Backspace: 
            self.logic.handle_key_press("BACKSPACE")
        elif key in "0123456789ABCDEF" and len(key) == 1: 
            self.logic.handle_key_press(key)
        elif event.key() in [Qt.Key.Key_Return, Qt.Key.Key_Enter]: 
            self.submit_final_guess()
        self._update_final_guess_display()

    def on_cell_clicked(self, index):
        if self.logic.is_game_over or index in self.logic.solved_indices: 
            self.main_notification_label.setText("This character is already solved or game is over!"); return
        
        self.current_clicked_index = index
        
        hex_char_for_minigame = self.logic.secret_color_code[index]
        
        self.nerdle_minigame_widget.start_new_minigame(hex_char_for_minigame)
        self.stacked_widget.setCurrentWidget(self.nerdle_minigame_widget)
        self.nerdle_minigame_widget.setFocus()

    def on_minigame_won(self, revealed_char):
        if self.current_clicked_index != -1:
            all_solved = self.logic.handle_minigame_win(self.current_clicked_index, revealed_char)
            label_to_update = self.hexle_labels[0][self.current_clicked_index]
            
            label_to_update.setText(revealed_char)
            label_to_update.setStyleSheet(ui.get_style_sheet(
                bg_color=config.COLOR_CORRECT_PLACE, 
                border_color=config.COLOR_CORRECT_PLACE, 
                bold=True))
            self.current_clicked_index = -1
            
        if all_solved: self._end_game(reason="win_all_puzzles")

    def on_minigame_cant_solve(self):
        if self.current_clicked_index != -1:
            self.logic.handle_minigame_give_up(self.current_clicked_index)
            label_to_update = self.hexle_labels[0][self.current_clicked_index]
            label_to_update.setText("X") 
            label_to_update.setStyleSheet(ui.get_style_sheet(
                bg_color=config.COLOR_GIVE_UP, 
                border_color=config.COLOR_GIVE_UP, 
                bold=True))
            self.current_clicked_index = -1    
        
        self.show_main_game_screen(); 
        self.main_notification_label.setText("You gave up or lose on that character.")
    
    def submit_final_guess(self):
        result = self.logic.submit_final_guess()
        if result['status'] == "invalid":
            self.main_notification_label.setText(result['message']); return
        
        current_row_labels = self.final_guess_labels[self.logic.final_guess_row - 1]
        color_map = {
            "correct_place": config.COLOR_CORRECT_PLACE,
            "correct_letter": config.COLOR_CORRECT_LETTER,
            "wrong_letter": config.COLOR_WRONG_LETTER
        }
        for i, color_key in enumerate(result['colors']):
            color_val = color_map[color_key]
            current_row_labels[i].setStyleSheet(ui.get_style_sheet(
                bg_color=color_val, 
                border_color=color_val, 
                bold=True))

        if result['status'] == 'win': self._end_game("win")
        elif result['status'] == 'lose': self._end_game("lose")
        else: self.main_notification_label.setText(result['message'])

    def handle_give_up(self):
        if not self.logic.is_game_over: self._end_game("gave_up")
    
    def _end_game(self, reason):
        title, message = "", ""
        
        reveal_text = f"\nThe correct hex code was: #{self.logic.secret_color_code}\n\nDo you want to play again?"
        
        if reason == "win": 
            title = "You Won!"; message = f"Congratulations! You found the correct code!\n{reveal_text}"
        elif reason == "win_all_puzzles": 
            title = "You Won!"; message = f"Amazing! You solved all the puzzles!\n{reveal_text}"
        elif reason == "lose": 
            title = "Game Over!"; message = f"You've run out of guesses!\n{reveal_text}"
        elif reason == "gave_up": 
            title = "You Gave Up!"; message = f"You have forfeited this round.\n{reveal_text}"
        
        self.main_notification_label.setText(title)
        
        popup = QMessageBox(self); popup.setWindowTitle(title); popup.setText(message)
        popup.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        popup.setDefaultButton(QMessageBox.StandardButton.Yes); response = popup.exec()
        
        if response == QMessageBox.StandardButton.Yes: 
            self.start_new_game()
        else: 
            self.close()

    def _update_final_guess_display(self):
        """Đồng bộ hóa lưới đoán cuối cùng với trạng thái trong logic."""
        for r_idx, row_data in enumerate(self.logic.final_guesses):
            for c_idx, char in enumerate(row_data):
                self.final_guess_labels[r_idx][c_idx].setText(char)

    def show_main_game_screen(self):
        self.stacked_widget.setCurrentWidget(self.main_game_widget)
        self.main_game_widget.setFocus()

def run():
    app = QApplication.instance() or QApplication(sys.argv)
    game = HexleGame()
    game.show()
    sys.exit(app.exec())