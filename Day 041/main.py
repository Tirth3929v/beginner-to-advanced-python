"""
Day 41 - Web Foundation: Introduction to HTML
Studio launcher providing HTML code inspection and a live local web server.
"""

import http.server
import os
import socketserver
import sys
import threading
import webbrowser
from art import logo

# Ensure UTF-8 output encoding for Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

PORT = 8041
HTML_FILE = os.path.join(os.path.dirname(__file__), "index.html")


def launch_web_server():
    """Starts local Python HTTP server and opens page in browser."""
    web_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(web_dir)

    handler = http.server.SimpleHTTPRequestHandler
    try:
        with socketserver.TCPServer(("", PORT), handler) as httpd:
            print(f"\n🚀 Local HTTP Web Server started at: http://localhost:{PORT}")
            print("🌐 Opening portfolio website in your browser...")
            webbrowser.open(f"http://localhost:{PORT}/index.html")
            print("Press Ctrl+C to stop server.\n")
            httpd.serve_forever()
    except OSError:
        print(f"ℹ️ Port {PORT} is busy, opening HTML file directly...")
        webbrowser.open(f"file://{os.path.abspath(HTML_FILE)}")
    except (KeyboardInterrupt, EOFError):
        print("\n👋 Web server stopped.")


def inspect_html():
    """Prints the raw HTML5 structure and highlights semantic elements."""
    if os.path.exists(HTML_FILE):
        print("\n" + "=" * 70)
        print(" 📄 HTML5 SOURCE CODE INSPECTOR (index.html)")
        print("=" * 70)
        with open(HTML_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
            for i, line in enumerate(lines[:35], 1):
                print(f" {i:2d} | {line.rstrip()}")
        print(" ... [Remaining lines omitted for display] ...")
        print("=" * 70 + "\n")


def main():
    print(logo)
    print("Welcome to Day 41 - Web Foundation & Semantic HTML5 Studio! 🌐📄\n")

    try:
        while True:
            print("Select an option:")
            print(" 1. 🚀 Launch Local Web Server & Preview HTML in Browser")
            print(" 2. 🔍 Inspect HTML5 Source Code & Semantic Tags")
            print(" 3. 🚪 Exit\n")

            choice = input("👉 Enter choice (1-3): ").strip()
            if choice == "1":
                launch_web_server()
            elif choice == "2":
                inspect_html()
            elif choice == "3":
                print("\nExiting Day 41 Studio... Happy coding! 👋\n")
                break
            else:
                print("⚠️ Invalid choice! Please select 1-3.\n")

    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Exiting Day 41 Studio gracefully... Goodbye!\n")


if __name__ == "__main__":
    main()
