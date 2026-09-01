import sys
from hirst_painting import generate_hirst_painting
from shapes_and_walk import draw_geometric_shapes, draw_random_walk, draw_spirograph

# Ensure UTF-8 output encoding for Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def main():
    """Main menu loop allowing user to select Turtle graphics generators."""
    print(r"""
  ╔══════════════════════════════════════════════════════════════════════════╗
  ║                                                                          ║
  ║      🎨   T U R T L E   G R A P H I C S   &   H I R S T   🎨            ║
  ║                                                                          ║
  ║            [ GUI Canvas • Tuples • Algorithmic Fine Art ]                ║
  ║                                                                          ║
  ╚══════════════════════════════════════════════════════════════════════════╝
""")
    
    print("Welcome to Day 18 - Turtle Graphics Studio! 🐢✨\n")
    print("Select a demo to launch:")
    print(" 1. 📐 Geometric Polygons (Triangle to Decagon)")
    print(" 2. 🔀 2D Random Walk Canvas")
    print(" 3. 🌀 Spirograph Generator")
    print(" 4. 🎨 Damien Hirst Spot Painting Generator (10x10)")
    print(" 5. 🚪 Exit\n")

    try:
        choice = input("👉 Enter choice (1-5): ").strip()
        if choice == "1":
            draw_geometric_shapes()
        elif choice == "2":
            draw_random_walk()
        elif choice == "3":
            draw_spirograph()
        elif choice == "4":
            generate_hirst_painting()
        elif choice == "5":
            print("Goodbye! 👋")
        else:
            print("Invalid choice! Defaulting to Damien Hirst Painting...")
            generate_hirst_painting()
    except Exception as e:
        print(f"\n⚠️ Note: GUI display requires interactive window environment. ({e})")


if __name__ == "__main__":
    main()
