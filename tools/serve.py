"""Local preview server for ./site with clean URLs and the 404 page.

    python tools/serve.py [port]      (default 5184) → http://localhost:5184/
Dev flags: ?motion=full (force animations even if the OS asks for reduced motion),
?motion=reduce, and &raw (native scrolling instead of Lenis). The motion choice is remembered
in localStorage — use ?motion=auto... or clear it via ?motion=reduce / full as needed.
"""
import functools
import http.server
import socketserver
import sys
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent / "site"


class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def send_error(self, code, message=None, explain=None):
        if code == 404 and (SITE / "404.html").exists():
            body = (SITE / "404.html").read_bytes()
            self.send_response(404)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        super().send_error(code, message, explain)


Handler.extensions_map.update({".js": "text/javascript", ".webp": "image/webp", ".svg": "image/svg+xml"})

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5184
    socketserver.ThreadingTCPServer.allow_reuse_address = True
    with socketserver.ThreadingTCPServer(("127.0.0.1", port), functools.partial(Handler, directory=str(SITE))) as httpd:
        print(f"Serving {SITE} at http://localhost:{port}/")
        httpd.serve_forever()
