"""
Day 83: Tic Tac Toe Python Game with Unbeatable AI
Interactive Console Game with Minimax Decision Search
"""

import sys
import os

# Ensure UTF-8 output encoding for Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from art import LOGO
from game_engine import TicTacToe


def banner():
    print(LOGO)
    print("=" * 76)
    print(" 🚀 DAY 83: TIC TAC TOE WITH UNBEATABLE MINIMAX DECISION AI")
    print(" 📚 Phase 4: Professional Portfolio Projects | 100 Days of Code Bootcamp")
    print("=" * 76)
    print(" Game Engine Architecture:")
    print("  • Adversarial Tree Search: Minimax algorithm prioritizing rapid victory")
    print("  • Terminal State Scoring: Depth penalization for optimal move choices")
    print("  • Dynamic Grid Rendering with ANSI Color Accents")
    print("  • Multi-mode Support: Human vs Unbeatable AI, 2-Player, and AI Simulation")
    print("=" * 76 + "\n")


def play_vs_ai():
    game = TicTacToe()
    print("\n⚔️ HUMAN (X) VS UNBEATABLE AI (O)")
    print("=" * 50)
    print("Enter numbers 1 to 9 corresponding to the board slots.")

    current_player = "X"
    while True:
        print(game.render_board())
        if current_player == "X":
            while True:
                choice = input("Your Move (1-9): ").strip()
                if choice.isdigit() and int(choice) in game.available_moves():
                    game.make_move(int(choice), "X")
                    break
                print("⚠️ Invalid move! Choose an available slot (1-9).")
        else:
            print("🤖 AI is calculating the optimal minimax move...")
            ai_move = game.get_best_ai_move(ai_player="O")
            game.make_move(ai_move, "O")
            print(f"-> AI placed 'O' at slot {ai_move}")

        over, winner = game.is_game_over()
        if over:
            print(game.render_board())
            if winner == "X":
                print("🎉 INCREDIBLE! You defeated the Minimax AI!\n")
            elif winner == "O":
                print("🤖 The AI claims victory! Optimal strategy prevails.\n")
            else:
                print("🤝 It's a draw! Perfect play on both sides.\n")
            break

        current_player = "O" if current_player == "X" else "X"


def play_two_player():
    game = TicTacToe()
    print("\n👥 2-PLAYER PASS & PLAY MODE")
    print("=" * 50)
    current_player = "X"

    while True:
        print(game.render_board())
        while True:
            choice = input(f"Player '{current_player}' Move (1-9): ").strip()
            if choice.isdigit() and int(choice) in game.available_moves():
                game.make_move(int(choice), current_player)
                break
            print("⚠️ Invalid move! Choose an empty slot (1-9).")

        over, winner = game.is_game_over()
        if over:
            print(game.render_board())
            if winner == "Tie":
                print("🤝 The game ended in a draw!\n")
            else:
                print(f"🎉 Congratulations! Player '{winner}' wins!\n")
            break

        current_player = "O" if current_player == "X" else "X"


def run_ai_simulation():
    game = TicTacToe()
    print("\n🤖 AI VS AI SELF-PLAY DEMONSTRATION")
    print("=" * 50)
    current = "X"

    while True:
        move = game.get_best_ai_move(ai_player=current)
        game.make_move(move, current)
        print(f"  • AI '{current}' selects slot {move}")

        over, winner = game.is_game_over()
        if over:
            print(game.render_board())
            print(f"Match Result: \033[93m{winner}\033[0m (Proven equilibrium under optimal play).\n")
            break
        current = "O" if current == "X" else "X"


def run_automated_tests():
    """Validates win logic, draw detection, and Minimax AI decision correctness."""
    print("\n🔍 Running Day 83 Automated Tic-Tac-Toe & Minimax Test Suite...")
    print("-" * 70)
    game = TicTacToe()

    # 1. Move making & clearing
    assert game.make_move(5, "X") is True
    assert game.make_move(5, "O") is False  # Cannot overwrite
    assert 5 not in game.available_moves()
    print(" [PASS] 1. Move validation and slot occupation verified.")

    # 2. Row win condition
    game.reset()
    for pos in [1, 2, 3]:
        game.make_move(pos, "X")
    assert game.check_winner("X") is True
    assert game.is_game_over() == (True, "X")
    print(" [PASS] 2. Horizontal row win detection verified.")

    # 3. Diagonal win condition
    game.reset()
    for pos in [1, 5, 9]:
        game.make_move(pos, "O")
    assert game.check_winner("O") is True
    print(" [PASS] 3. Diagonal win detection verified.")

    # 4. Tie detection
    game.reset()
    # X O X / X O O / O X X
    moves = [(1, 'X'), (2, 'O'), (3, 'X'), (4, 'X'), (5, 'O'), (6, 'O'), (7, 'O'), (8, 'X'), (9, 'X')]
    for pos, player in moves:
        game.make_move(pos, player)
    assert game.is_game_over() == (True, "Tie")
    print(" [PASS] 4. Draw / Tie game state verified.")

    # 5. Minimax AI: Immediate winning move selection
    game.reset()
    game.make_move(1, "O")
    game.make_move(2, "O")
    # Slot 3 is the winning move for O
    best_move = game.get_best_ai_move(ai_player="O")
    assert best_move == 3, f"Expected AI to take winning slot 3, chose {best_move}"
    print(" [PASS] 5. Minimax immediate victory exploitation verified.")

    # 6. Minimax AI: Immediate block of opponent victory
    game.reset()
    game.make_move(4, "X")
    game.make_move(5, "X")
    # Slot 6 must be blocked by O
    block_move = game.get_best_ai_move(ai_player="O")
    assert block_move == 6, f"Expected AI to block human threat at slot 6, chose {block_move}"
    print(" [PASS] 6. Minimax defensive blocking verified.")

    print("-" * 70)
    print("✨ ALL 6 TESTS PASSED! Minimax Game Engine fully operational.\n")


def main():
    banner()
    while True:
        print("Select a game mode:")
        print("  1) ⚔️ Play vs Unbeatable AI (Human 'X' vs AI 'O')")
        print("  2) 👥 Play 2-Player Pass & Play (Local)")
        print("  3) 🤖 AI vs AI Optimal Play Simulation")
        print("  4) ✅ Run Automated Verification Suite (6 Unit Tests)")
        print("  5) 🚪 Exit")
        choice = input("\nEnter your choice (1-5): ").strip()

        if choice == "1":
            play_vs_ai()
        elif choice == "2":
            play_two_player()
        elif choice == "3":
            run_ai_simulation()
        elif choice == "4":
            run_automated_tests()
        elif choice in ("5", "exit", "quit", "q"):
            print("\n👋 Good game! Thanks for playing! ⚔️\n")
            break
        else:
            print("⚠️ Invalid choice. Please select 1-5.\n")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Exiting Day 83 gracefully... Goodbye!\n")
