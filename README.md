# Minesweeper AI Solver

<img src="https://github.com/apiyarali/Minesweeper-AI-Solver/blob/111318f8fcae79205fc2748444014148e3834e94/assets/images/minesweeper_card.png" alt="Minesweeper AI Game" width="300">

## Overview
This project implements an AI solver for the classic Minesweeper game using propositional logic and inference techniques. The AI plays the game by making logical deductions about which cells contain mines and which are safe based on the numbers revealed in adjacent cells. By maintaining a knowledge base of logical sentences, the AI can iteratively refine its understanding of the board to make informed moves.

## Files
- **minesweeper.py**: Implements the core game logic, AI inference system, and knowledge representation.
- **runner.py**: Provides a graphical interface for playing Minesweeper and testing the AI.

## How It Works
The AI follows a knowledge-based approach:
1. **Representation of Knowledge**
   - Each sentence consists of a set of board cells and a count of how many of them are mines.
   - Example: `{A, B, C} = 1` means exactly one of A, B, or C is a mine.

2. **Inference and Deduction**
   - If `{X, Y, Z} = 0`, then all of X, Y, and Z are safe.
   - If `{P, Q, R} = 3`, then all of P, Q, and R must be mines.
   - If two sentences exist where one is a subset of another, the AI can infer new knowledge.

3. **Decision Making**
   - The AI marks known mines and safe cells based on knowledge.
   - If a safe move is available, it chooses that.
   - If no safe move is certain, it makes a random move to continue the game.

## Running the AI
To run the Minesweeper AI, execute the following command:
```sh
python runner.py
```
The graphical interface will start, allowing the AI to play the game automatically.

## AI Components
### Minesweeper Class
Handles game mechanics, randomly generating mine placements and evaluating user or AI moves.

### Sentence Class
Represents a logical sentence containing:
- A set of board cells.
- A count of how many are mines.
- Methods to infer known mines and safe cells.

### MinesweeperAI Class
Maintains the AI's knowledge and determines optimal moves:
- **add_knowledge(cell, count)**: Updates knowledge based on revealed information.
- **make_safe_move()**: Selects a move that is guaranteed to be safe.
- **make_random_move()**: Chooses a random move if no safe moves exist.

## Features
- **Logical Deduction**: Uses propositional logic to determine mines and safe spaces.
- **Efficient Knowledge Representation**: Stores sentences that dynamically update as the game progresses.
- **AI Decision Making**: Prioritizes safe moves and only resorts to guessing when necessary.
- **Graphical Interface**: Allows users to watch the AI play in real time.

## Notes
- The AI may sometimes need to guess, as Minesweeper contains cases where logical inference alone is insufficient.
- The game board size and mine count can be adjusted in `runner.py`.

## Credits
Inspired by Harvard's CS80 AI course and the logical deduction techniques used in classic Minesweeper AI implementations.

