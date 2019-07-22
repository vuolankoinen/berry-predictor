from http.server import HTTPServer, BaseHTTPRequestHandler
import os
from keras.models import load_model
import pandas as pd

class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        # prediction_text = 'Berry prediction:\nAt this time, the predicted amount of lingonberries to reach sales in Lapland is {} tons.'.format(pred_lingonberries()[0][0])
        self.wfile.write(prediction_text.encode())
        # self.wfile.write(list_dirs().encode())
        self.wfile.write((os.getcwd() + '\n').encode())
        self.wfile.write(b'Toimii jotenkin.')
        os.chdir('..')
        self.wfile.write((os.getcwd() + '\n').encode())
        # self.wfile.write(list_dirs().encode())
        self.wfile.write(("\n" + list_dir('.') + "\n").encode())
        self.wfile.write(("\n" + list_dir('..') + "\n").encode())

def list_files():
    res = ""
    for root, dirs, files in os.walk("."):
        for filename in files:
            res = res + "\n" + filename
    #for r, d, f in os.walk("../data"):
    return res

def list_dirs():
    res = ""
    # for root, dirs, files in os.walk("."):
    root, dirs, files = os.walk(".")
    for d in dirs:
        res = res + "\n" + d
    #for r, d, f in os.walk("../data"):
    return res

def start_server():
    HTTPServer(('', int(os.environ['PORT'])), Server).serve_forever()

def pred_lingonberries():
    net = load_model('../src/nnet/Lingonberry-Lapland.net')
    recent = pd.read_csv('../data/recent.csv')
    rec = pd.DataFrame(columns=range(0, len(recent)))
    rec.loc[0] = list(recent.iloc[:, 1])
    return(net.predict(rec))

if __name__ == "__main__":
    start_server()
