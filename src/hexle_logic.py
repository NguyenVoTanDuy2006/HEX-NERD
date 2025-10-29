import random
from collections import Counter

class HexleGameLogic:
    MAX_FINAL_GUESSES = 4

    def __init__(self):
        self.secret_color_code = ""
        self.is_game_over = False
        self.final_guess_row = 0
        self.final_guess_col = 0
        self.solved_indices = set()
        self.won_indices = set()
        self.final_guesses = [[""] * 6 for _ in range(self.MAX_FINAL_GUESSES)]

    def start_new_game(self):
        self.secret_color_code = f"{random.randint(0, 0xFFFFFF):06X}"
        self.is_game_over = False
        self.final_guess_row = 0
        self.final_guess_col = 0
        self.solved_indices.clear()
        self.won_indices.clear()
        self.final_guesses = [[""] * 6 for _ in range(self.MAX_FINAL_GUESSES)]

    def handle_key_press(self, key):
        if key == "BACKSPACE":
            if self.final_guess_col > 0:
                self.final_guess_col -= 1
                self.final_guesses[self.final_guess_row][self.final_guess_col] = ""
        elif key in "0123456789ABCDEF":
            if self.final_guess_col < 6:
                self.final_guesses[self.final_guess_row][self.final_guess_col] = key
                self.final_guess_col += 1

    def handle_minigame_win(self, index, char):
        self.solved_indices.add(index)
        self.won_indices.add(index)
        return len(self.won_indices) == 6

    def handle_minigame_give_up(self, index):
        self.solved_indices.add(index)

    def submit_final_guess(self):
        if self.final_guess_col != 6:
            return {"status": "invalid", "message": "Not enough characters for a full guess."}

        guess_str = "".join(self.final_guesses[self.final_guess_row])
        secret = self.secret_color_code
        
        # Logic tô màu
        temp_secret_counts = Counter(secret)
        colors = [""] * 6
        for i in range(6):
            if guess_str[i] == secret[i]:
                colors[i] = "correct_place"
                temp_secret_counts[guess_str[i]] -= 1
        
        for i in range(6):
            if colors[i] == "":
                if guess_str[i] in temp_secret_counts and temp_secret_counts[guess_str[i]] > 0:
                    colors[i] = "correct_letter"
                    temp_secret_counts[guess_str[i]] -= 1
                else:
                    colors[i] = "wrong_letter"

        self.final_guess_row += 1
        self.final_guess_col = 0
        
        # Kiểm tra thắng/thua
        if guess_str == secret:
            self.is_game_over = True
            return {"status": "win", "colors": colors}


        if self.final_guess_row == self.MAX_FINAL_GUESSES:
            self.is_game_over = True
            return {"status": "lose", "colors": colors}
        
        return {"status": "continue", "colors": colors, "message": "Incorrect. Try again!"}