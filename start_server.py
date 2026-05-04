#!/usr/bin/env python3
"""
AVI → MP4 Converter – Lokaler Server
=====================================
Führe dieses Skript aus, um den Converter zu starten:

  Windows:  Doppelklick auf start_server.py  ODER  python start_server.py
  Mac/Linux: python3 start_server.py

Der Browser öffnet sich automatisch.
"""

import http.server
import threading
import webbrowser
import os
import sys

PORT = 8765
HTML_FILE = "index.html"

class CORSHandler(http.server.SimpleHTTPRequestHandler):
    """Serves files with headers required for ffmpeg.wasm (SharedArrayBuffer)."""

    def end_headers(self):
        # These two headers are REQUIRED for ffmpeg.wasm to work
        self.send_header("Cross-Origin-Opener-Policy",   "same-origin")
        self.send_header("Cross-Origin-Embedder-Policy", "require-corp")
        self.send_header("Access-Control-Allow-Origin",  "*")
        super().end_headers()

    def log_message(self, format, *args):
        # Suppress noisy request logs
        pass

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    if not os.path.exists(HTML_FILE):
        print(f"FEHLER: '{HTML_FILE}' nicht gefunden.")
        print(f"Stelle sicher, dass beide Dateien im selben Ordner liegen.")
        input("Enter drücken zum Beenden...")
        sys.exit(1)

    url = f"http://localhost:{PORT}/{HTML_FILE}"

    server = http.server.HTTPServer(("", PORT), CORSHandler)

    print("=" * 50)
    print("  AVI → MP4 Converter")
    print("=" * 50)
    print(f"  Server läuft auf: {url}")
    print(f"  Stoppen: Strg+C (oder Fenster schließen)")
    print("=" * 50)

    # Open browser after short delay
    threading.Timer(1.0, lambda: webbrowser.open(url)).start()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer gestoppt.")

if __name__ == "__main__":
    main()
