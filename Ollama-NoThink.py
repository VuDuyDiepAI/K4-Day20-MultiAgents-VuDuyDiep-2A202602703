"""Loopback-only Ollama adapter: disable thinking without changing lab prompts."""
import json
import http.client
import select
import socket
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

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
        upstream = http.client.HTTPConnection('127.0.0.1', 11434, timeout=600)
        finished = threading.Event()

        def watch_disconnect():
            while not finished.wait(0.1):
                try:
                    readable, _, _ = select.select([self.connection], [], [], 0)
                    if readable and not self.connection.recv(1, socket.MSG_PEEK):
                        if upstream.sock is not None:
                            upstream.sock.shutdown(socket.SHUT_RDWR)
                        return
                except OSError:
                    return

        try:
            upstream.request(self.command, self.path, body=body if body else None,
                             headers={'Content-Type': 'application/json'})
            threading.Thread(target=watch_disconnect, daemon=True).start()
            response = upstream.getresponse()
            self.send_response(response.status)
            self.send_header('Content-Type', response.headers.get('Content-Type', 'application/json'))
            self.send_header('Connection', 'close')
            self.end_headers()
            while chunk := response.read1(65536):
                self.wfile.write(chunk)
                self.wfile.flush()
        except (OSError, http.client.HTTPException):
            try:
                self.send_error(502, 'Ollama request interrupted or unavailable')
            except OSError:
                pass
        finally:
            finished.set()
            upstream.close()
            self.close_connection = True


if __name__ == '__main__':
    ThreadingHTTPServer(('127.0.0.1', 11435), Handler).serve_forever()
