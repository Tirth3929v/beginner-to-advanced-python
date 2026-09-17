"""
Day 43 - Web Foundation: Introduction to CSS
Studio launcher to inspect external stylesheet rules and launch local browser server.
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

PORT = 8043
HTML_FILE = os.path.join(os.path.dirname(__file__), "index.html")


def launch_web_server():
    """Starts local Python HTTP server and opens page in browser."""
    web_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(web_dir)

    handler = http.server.SimpleHTTPRequestHandler
    try:
        with socketserver.TCPServer(("", PORT), handler) as httpd:
            print(f"\n🚀 Local HTTP Web Server started at: http://localhost:{PORT}")
            print("🌐 Opening CSS3 Styling Studio in your browser...")
            webbrowser.open(f"http://localhost:{PORT}/index.html")
            print("Press Ctrl+C to stop server.\n")
            httpd.serve_forever()
    except OSError:
        print(f"ℹ️ Port {PORT} is busy, opening HTML file directly...")
        webbrowser.open(f"file://{os.path.abspath(HTML_FILE)}")
    except (KeyboardInterrupt, EOFError):
        print("\n👋 Web server stopped.")


def explain_css_box_model():
    """Prints a visual ASCII representation of the CSS Box Model."""
    print("\n" + "=" * 70)
    print(" 📦 THE CSS BOX MODEL ARCHITECTURE")
    print("=" * 70)
    print(r"""
  ┌─────────────────────────────────────────────────────────────┐
  │ MARGIN (Clear space outside border)                         │
  │   ┌─────────────────────────────────────────────────────────┐
  │   │ BORDER (Decorative line boundary)                       │
  │   │   ┌─────────────────────────────────────────────────────┐
  │   │   │ PADDING (Internal buffer between border & text)     │
  │   │   │   ┌─────────────────────────────────────────────────┐
  │   │   │   │ CONTENT (The text, image, or nested element)    │
  │   │   │   └─────────────────────────────────────────────────┘
  │   │   └─────────────────────────────────────────────────────┘
  │   └─────────────────────────────────────────────────────────┘
  └─────────────────────────────────────────────────────────────┘
    """)
    print("Tip: Use 'box-sizing: border-box;' so padding does not expand element width!\n")
    print("=" * 70 + "\n")


def main():
    print(logo)
    print("Welcome to Day 43 - Introduction to CSS3 Studio! 🎨✨\n")

    try:
        while True:
            print("Select an option:")
            print(" 1. 🚀 Launch Local Web Server & Preview CSS in Browser")
            print(" 2. 📦 View Visual CSS Box Model Guide")
            print(" 3. 🚪 Exit\n")

            choice = input("👉 Enter choice (1-3): ").strip()
            if choice == "1":
                launch_web_server()
            elif choice == "2":
                explain_css_box_model()
            elif choice == "3":
                print("\nExiting Day 43 Studio... Happy styling! 👋\n")
                break
            else:
                print("⚠️ Invalid choice! Please select 1-3.\n")

    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Exiting Day 43 Studio gracefully... Goodbye!\n")


if __name__ == "__main__":
    main()
