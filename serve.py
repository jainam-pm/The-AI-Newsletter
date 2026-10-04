#!/usr/bin/env python3
import http.server
import socketserver
import os
import sys

PORT = 8000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

print(f"Working directory: {DIRECTORY}")
print(f"Files in output/: {os.listdir(os.path.join(DIRECTORY, 'output'))}")

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def log_message(self, format, *args):
        print(f"[{self.client_address[0]}] {format % args}")

try:
    with socketserver.TCPServer(("0.0.0.0", PORT), MyHandler) as httpd:
        print(f"\n✓ Server running at http://localhost:{PORT}")
        print(f"✓ Open: http://localhost:8000/output/2026-10-04-fixed.html")
        print(f"✓ Or: http://127.0.0.1:8000/output/2026-10-04-fixed.html")
        print("\nPress Ctrl+C to stop\n")
        httpd.serve_forever()
except OSError as e:
    print(f"Error: {e}")
    print("Port 8000 may be in use. Try a different port or close other apps.")
    sys.exit(1)
