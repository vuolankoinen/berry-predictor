from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
import os

class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Toimii jotenkin.')

def start_server():
    HTTPServer(('', int(os.environ['PORT'])), Server).serve_forever()

if __name__ == "__main__":
    start_server()


#import tornado.ioloop
#import tornado.web
#import os
#
#class MainHandler(tornado.web.RequestHandler):
#    def get(self):
#        self.write("Toimii jotankin.")
#
#def make_app():
#    return tornado.web.Application([
#        (r"/", MainHandler),
#    ])
#
#if __name__ == "__main__":
#    app = make_app()
#    app.listen(os.environ['PORT'])
#    tornado.ioloop.IOLoop.current().start()
#
