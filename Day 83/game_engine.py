"""
Day 83: Tic Tac Toe Game Engine & Unbeatable Minimax AI
Deterministic game tree search ensuring optimal adversarial gameplay.
"""

from typing import List, Optional, Tuple


class TicTacToe:
    def __init__(self):
        # 1-indexed board (0 unused, indices 1 to 9)
        self.board: List[str] = [" "] * 10

    def reset(self):
        self.board = [" "] * 10

    def make_move(self, position: int, player: str) -> bool:
        if 1 <= position <= 9 and self.board[position] == " ":
            self.board[position] = player
            return True
        return False

    def undo_move(self, position: int):
        if 1 <= position <= 9:
            self.board[position] = " "

    def available_moves(self) -> List[int]:
        return [i for i in range(1, 10) if self.board[i] == " "]

    def is_board_full(self) -> bool:
        return " " not in self.board[1:]

    def check_winner(self, player: str) -> bool:
        win_combos = [
            (1, 2, 3), (4, 5, 6), (7, 8, 9),  # Rows
            (1, 4, 7), (2, 5, 8), (3, 6, 9),  # Columns
            (1, 5, 9), (3, 5, 7)              # Diagonals
        ]
        return any(self.board[a] == self.board[b] == self.board[c] == player for a, b, c in win_combos)

    def is_game_over(self) -> Tuple[bool, Optional[str]]:
        """Returns (is_over, winner_or_None_or_'Tie')."""
        if self.check_winner("X"):
            return True, "X"
        if self.check_winner("O"):
            return True, "O"
        if self.is_board_full():
            return True, "Tie"
        return False, None

    def render_board(self) -> str:
        """Renders stylized 3x3 grid with slot numbers if empty."""
        def slot(i: int) -> str:
            val = self.board[i]
            if val == "X":
                return "\033[94mX\033[0m"
            elif val == "O":
                return "\033[91mO\033[0m"
            else:
                return f"\033[90m{i}\033[0m"

        return f"""
         {slot(1)} | {slot(2)} | {slot(3)}
        ---+---+---
         {slot(4)} | {slot(5)} | {slot(6)}
        ---+---+---
         {slot(7)} | {slot(8)} | {slot(9)}
        """

    def minimax(self, depth: int, is_maximizing: bool, ai_player: str, human_player: str) -> int:
        """
        Recursive Minimax implementation.
        Max score +10 for AI win, -10 for Human win, 0 for tie.
        Depth deduction incentivizes rapid victory and prolonged defense.
        """
        if self.check_winner(ai_player):
            return 10 - depth
        if self.check_winner(human_player):
            return depth - 10
        if self.is_board_full():
            return 0

        if is_maximizing:
            best_score = -float("inf")
            for move in self.available_moves():
                self.make_move(move, ai_player)
                score = self.minimax(depth + 1, False, ai_player, human_player)
                self.undo_move(move)
                best_score = max(score, best_score)
            return int(best_score)
        else:
            best_score = float("inf")
            for move in self.available_moves():
                self.make_move(move, human_player)
                score = self.minimax(depth + 1, True, ai_player, human_player)
                self.undo_move(move)
                best_score = min(score, best_score)
            return int(best_score)

    def get_best_ai_move(self, ai_player: str = "O") -> int:
        """Determines the optimal move for AI using Minimax."""
        human_player = "X" if ai_player == "O" else "O"
        best_score = -float("inf")
        best_move = self.available_moves()[0]

        for move in self.available_moves():
            self.make_move(move, ai_player)
            score = self.minimax(0, False, ai_player, human_player)
            self.undo_move(move)
            if score > best_score:
                best_score = score
                best_move = move

        return best_move
