# Hex-Nerd Game with PyQt5

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A fully-featured clone of the popular word-guessing game, Wordle, built with Python and the PyQt6 GUI framework. This project emphasizes a clean, modular architecture (Model-View-Controller pattern) and utilizes modern Python tooling with `uv` for package management.


---

## 📜 Table of Contents

- [✨ Key Features](#-key-features)
- [🛠️ Tech Stack](#-tech-stack)
- [🏗️ Project Structure](#️-project-structure)
- [🚀 Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation & Running](#installation--running)
- [🎮 How to Play](#-how-to-play)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

## ✨ Key Features

-   **Rich Graphical User Interface**: A polished and intuitive UI built with PyQt6.
-   **Dual Input Support**: Play using either your physical keyboard or the on-screen virtual keyboard.
-   **Dynamic Feedback**: Instant color-coded feedback for each guessed letter.
-   **State Management**: Includes "Give Up" functionality and a clear end-game dialog with an option to play again.
-   **Modular Architecture**: The code is cleanly separated into distinct modules for game logic, UI components, and configuration, making it easy to maintain and extend.

## 🛠️ Tech Stack

-   **Language**: Python
-   **GUI Framework**: PyQt6
-   **Package Manager**: [**`uv`**](https://github.com/astral-sh/uv) - An extremely fast Python package installer and resolver.

## 🏗️ Project Structure

This project follows a well-organized structure to separate concerns, making the codebase clean and scalable.

Of course, here is the directory tree with notes in English:

```
📦src
 ┣ 📜config.py            # Stores color constants and the global stylesheet for the entire application.
 ┣ 📜generate_nerdle.py    # Contains the logic to generate random problems for the Nerdle minigame.
 ┣ 📜hexle.py             # The main file for the Hexle game, managing the window, main game flow, and screen transitions.
 ┣ 📜hexle_logic.py       # Separates the core Hexle game logic (state, guessing, win/loss) from the UI.
 ┣ 📜main.py             # The application's entry point, which initializes and runs the game.
 ┣ 📜nerdle.py            # Builds the user interface (UI) and handles events for the Nerdle minigame.
 ┣ 📜nerdle_logic.py      # Separates the logic for the Nerdle minigame (state, equation validation) from the UI.
 ┗ 📜ui.py               # Contains utility functions and classes for creating reusable UI components (e.g., grids, color squares, notification labels).
```

## 🚀 Getting Started

Follow these instructions to get a copy of the project up and running on your local machine.

### Prerequisites

You need to have **Git** and **`uv`** installed on your system.
-   [Git Installation Guide](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
-   [**`uv` Installation Guide**](https://github.com/astral-sh/uv#installation) (usually a single command)

### Installation & Running

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/NguyenVoTanDuy2006/HEX-NERD.git
    cd "HEX-NERD"
    ```

2.  **Create and activate a virtual environment using `uv`:**
    ```bash
    uv venv
    ```
    This will create a `.venv` directory. Activate it:
    -   On **macOS / Linux**: `source .venv/bin/activate`
    -   On **Windows**: `.venv\Scripts\activate`

3.  **Install the required dependencies using `uv`:**
    ```bash
    uv pip install -r requirements.txt
    ```
5.  **Run the game:**
    ```bash
    python src/main.py
    ```

## 🎮 How to Play

Hexle is a game of two parts: solving puzzles to get clues, and using those clues to make a final guess.

### Part 1: Reveal the Clues by Solving Puzzles

1.  **The Goal**: Your main objective is to guess the 6-digit hex code, which is displayed as a solid color block at the top.
2.  **Start with a Mystery**: The secret code is initially hidden behind six `?` blocks. Each `?` represents one character of the code (`0-9`, `A-F`).

    ![Image of the initial game board with ? blocks]
    *(Optional: Add a screenshot here)*

3.  **Launch a Minigame**: To get a clue, click on any `?` block. This will start a "Nerdle"-style math puzzle.

4.  **Solve the Math Puzzle**: In the minigame, you'll see a simple math equation with two missing 2-digit numbers (e.g., `[__] + [__] = 45`). Your goal is to fill in the blanks correctly. You have 6 attempts.
    *   **Green**: A digit is correct and in the right place.
    *   **Yellow**: A digit is correct but in the wrong place.
    *   **Gray**: A digit is not part of the answer.

5.  **Earn Your Hint**:
    *   ✅ If you **win** the puzzle, the `?` you clicked will be replaced by the correct character from the secret hex code.
    *   ❌ If you **lose** or **give up**, the block is marked with an `X`. You won't know what that character is, making the final guess harder.

You can solve as many or as few puzzles as you like before making a final guess.

### Part 2: Make Your Final Guess

1.  **Time to Guess**: Once you have enough clues (or if you just feel lucky!), you can type your 6-digit guess into the main grid at the bottom of the screen.

2.  **Submit and Get Feedback**: Press **Enter** to submit your guess. The tiles will change color to give you feedback, just like in Wordle:
    *   🟩 **Green `(correct_place)`**: The character is correct and in the right position.
    *   🟨 **Yellow `(correct_letter)`**: The character is in the secret code, but in a different position.
    *   ⬜ **Gray `(wrong_letter)`**: The character is not in the secret code at all.

3.  **Win or Lose**:
    *   🏆 **You win** by guessing the full hex code correctly within the 4 allowed attempts.
    *   💔 **You lose** if you run out of final guesses. You can start a new game at any time

## 🤝 Contributing

Contributions are welcome! If you have suggestions for improvements or find a bug, please feel free to open an issue or submit a pull request.

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request