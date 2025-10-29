# nerdle_logic.py

from collections import Counter
import generate_nerdle

class NerdleLogic:
    MAX_GUESSES = 6

    def __init__(self):
        self.secret_n1, self.secret_n2 = "", ""
        self.operator, self.result = "", ""
        self.current_row, self.current_col = 0, 0
        self.is_game_over = False
        self.guesses = [[""] * 4 for _ in range(self.MAX_GUESSES)]

    def start_new_minigame(self):
        self.secret_n1, self.secret_n2, self.operator, self.result = generate_nerdle.gen_problem()
        self.current_row, self.current_col = 0, 0
        self.is_game_over = False
        self.guesses = [[""] * 4 for _ in range(self.MAX_GUESSES)]

    def handle_key_press(self, key):

        if key == "BACKSPACE":
            if self.current_col > 0:
                self.current_col -= 1
                self.guesses[self.current_row][self.current_col] = ""
        elif key in "0123456789":
            if self.current_col < 4:
                self.guesses[self.current_row][self.current_col] = key
                self.current_col += 1

    def submit_guess(self):
        if self.current_col != 4:
            return {"status": "invalid", "message": "Not enough digits"}

        guess_n1 = self.guesses[self.current_row][0] + self.guesses[self.current_row][1]
        guess_n2 = self.guesses[self.current_row][2] + self.guesses[self.current_row][3]
        
        guess_str = guess_n1 + guess_n2
        secret_str = self.secret_n1 + self.secret_n2
        
        temp_secret_counts = Counter(secret_str)
        colors = [""] * 4
        for i in range(4):
            if guess_str[i] == secret_str[i]:
                colors[i] = "correct_place"
                temp_secret_counts[guess_str[i]] -= 1
        
        for i in range(4):
            if colors[i] == "":
                if guess_str[i] in temp_secret_counts and temp_secret_counts[guess_str[i]] > 0:
                    colors[i] = "correct_letter"
                    temp_secret_counts[guess_str[i]] -= 1
                else:
                    colors[i] = "wrong_letter"

        self.current_row += 1
        self.current_col = 0
        
        commutative = (self.operator == '+' or self.operator == '*')
        is_win = (guess_n1 == self.secret_n1 and guess_n2 == self.secret_n2) or \
                 (commutative and guess_n1 == self.secret_n2 and guess_n2 == self.secret_n1)

        if is_win:
            self.is_game_over = True
            return {"status": "win", "colors": colors}

        if self.current_row == self.MAX_GUESSES:
            self.is_game_over = True
            return {"status": "lose", "colors": colors}
        
        return {"status": "continue", "colors": colors, "message": "Try again!"}