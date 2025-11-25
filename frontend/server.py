#!/usr/bin/env python3
"""
Servidor HTTP simple que siempre sirve index.html en la raíz
"""
import http.server
import socketserver
from urllib.parse import urlparse

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Si la URL es la raíz o solo "/", servir index.html
        parsed_path = urlparse(self.path)
        if parsed_path.path == '/' or parsed_path.path == '':
            self.path = '/index.html'
        return super().do_GET()

    def end_headers(self):
        # Agregar headers para evitar caché en desarrollo
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        self.send_header('Last-Modified', '0')
        super().end_headers()

if __name__ == '__main__':
    PORT = 8080
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        print(f"🚀 Servidor iniciado en http://127.0.0.1:{PORT}")
        print(f"📝 La raíz (/) siempre mostrará index.html")
        print(f"🛑 Presiona Ctrl+C para detener el servidor")
        httpd.serve_forever()

