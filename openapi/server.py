import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler


class Handler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        super().end_headers()


port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000

print(f"Serving on http://localhost:{port}")

HTTPServer(("", port), Handler).serve_forever()