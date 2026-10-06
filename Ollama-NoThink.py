"""Loopback-only Ollama adapter: disable thinking without changing lab prompts."""
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.error import HTTPError
from urllib.request import Request, urlopen

UPSTREAM = 'http://127.0.0.1:11434'


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *_args):
        pass

    def do_GET(self):
        if self.path == '/lab-config':
            body = json.dumps({'think': False, 'upstream': UPSTREAM}).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        self.forward()

    def do_POST(self):
        self.forward()

    def forward(self):
        body = self.rfile.read(int(self.headers.get('Content-Length', '0')))
        if self.path.rstrip('/') == '/api/chat' and body:
            payload = json.loads(body)
            payload['think'] = False
            body = json.dumps(payload).encode('utf-8')
        request = Request(UPSTREAM + self.path, data=body if body else None,
                          headers={'Content-Type': 'application/json'}, method=self.command)
        try:
            response = urlopen(request, timeout=600)
        except HTTPError as exc:
            response = exc
        except OSError:
            self.send_error(502, 'Ollama upstream unavailable')
            return
        with response:
            self.send_response(response.status)
            self.send_header('Content-Type', response.headers.get('Content-Type', 'application/json'))
            self.send_header('Connection', 'close')
            self.end_headers()
            try:
                while chunk := response.read1(65536):
                    self.wfile.write(chunk)
                    self.wfile.flush()
            except (BrokenPipeError, ConnectionResetError):
                pass
        self.close_connection = True


if __name__ == '__main__':
    ThreadingHTTPServer(('127.0.0.1', 11435), Handler).serve_forever()
