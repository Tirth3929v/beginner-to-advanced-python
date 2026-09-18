"""
Day 44 - Web Foundation: Intermediate CSS & Flexbox
Studio launcher to inspect flexbox architecture and launch local browser server.
"""

import http.server
import os
import socketserver
import sys
import webbrowser
from art import logo

# Ensure UTF-8 output encoding for Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

PORT = 8044
HTML_FILE = os.path.join(os.path.dirname(__file__), "index.html")


def launch_web_server():
    """Starts local Python HTTP server and opens page in browser."""
    web_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(web_dir)

    handler = http.server.SimpleHTTPRequestHandler
    try:
        with socketserver.TCPServer(("", PORT), handler) as httpd:
            print(f"\n🚀 Local HTTP Web Server started at: http://localhost:{PORT}")
            print("🌐 Opening Responsive Flexbox Layout in your browser...")
            webbrowser.open(f"http://localhost:{PORT}/index.html")
            print("Press Ctrl+C to stop server.\n")
            httpd.serve_forever()
    except OSError:
        print(f"ℹ️ Port {PORT} is busy, opening HTML file directly...")
        webbrowser.open(f"file://{os.path.abspath(HTML_FILE)}")
    except (KeyboardInterrupt, EOFError):
        print("\n👋 Web server stopped.")


def explain_flexbox():
    """Prints a reference guide to CSS Flexbox parent and child properties."""
    print("\n" + "=" * 70)
    print(" 📐 CSS FLEXBOX QUICK REFERENCE GUIDE")
    print("=" * 70)
    print("""
 1. Container (Parent) Properties:
    - display: flex;                     (Activates flex layout)
    - flex-direction: row | column;      (Defines primary axis direction)
    - justify-content: center | space-between | space-around; (Aligns on main axis)
    - align-items: center | flex-start | flex-end; (Aligns on cross axis)
    - flex-wrap: wrap | nowrap;          (Allows elements to wrap onto new lines)
    - gap: 20px;                         (Sets clean space between items)

 2. Item (Child) Properties:
    - flex: 1 1 300px;                   (flex-grow, flex-shrink, flex-basis)
    - align-self: center;                (Overrides container alignment for one item)
    - order: 1;                          (Re-orders items visually without touching HTML)
    """)
    print("=" * 70 + "\n")


def main():
    print(logo)
    print("Welcome to Day 44 - Responsive CSS & Flexbox Studio! 📐📱\n")

    try:
        while True:
            print("Select an option:")
            print(" 1. 🚀 Launch Local Web Server & Preview Flexbox in Browser")
            print(" 2. 📚 View CSS Flexbox Quick Reference Guide")
            print(" 3. 🚪 Exit\n")

            choice = input("👉 Enter choice (1-3): ").strip()
            if choice == "1":
                launch_web_server()
            elif choice == "2":
                explain_flexbox()
            elif choice == "3":
                print("\nExiting Day 44 Studio... Keep building clean layouts! 👋\n")
                break
            else:
                print("⚠️ Invalid choice! Please select 1-3.\n")

    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Exiting Day 44 Studio gracefully... Goodbye!\n")


if __name__ == "__main__":
    main()
