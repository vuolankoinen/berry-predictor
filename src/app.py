from http.server import HTTPServer, BaseHTTPRequestHandler
import os
from keras.models import load_model

class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Toimii jotenkin.')

def start_server():
    HTTPServer(('', int(os.environ['PORT'])), Server).serve_forever()

if __name__ == "__main__":
    start_server()
