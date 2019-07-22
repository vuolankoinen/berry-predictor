from http.server import HTTPServer, BaseHTTPRequestHandler
import os
from keras.models import load_model
import pandas as pd

class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        prediction_test = ""
        try:
            prediction_text = 'Berry prediction:\nAt this time, the predicted amount of lingonberries to reach sales in Lapland is {} tons.'.format(pred_lingonberries()[0][0])
        except:
            prediction_text = prediction_test + 'File not found at ../src/nnet/'
        try:
            net = load_model('./nnet/Lingonberry-Lapland.net')
        except:
            prediction_text = 'File not found at ./nnet/'
        self.wfile.write(prediction_text.encode())
        # self.wfile.write(list_dirs().encode())
        self.wfile.write((os.getcwd() + '\n').encode())
        self.wfile.write(b'Toimii jotenkin.')
        os.chdir('..')
        self.wfile.write((os.getcwd() + '\n').encode())
        # self.wfile.write(list_dirs().encode())
        self.wfile.write(("<p>listdir .: " + list_dir('.') + "</p>").encode())
        self.wfile.write(("<p>listdir ..:" + list_dir('..') + "</p>").encode())

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
    r = os.walk(".")
    for d in r[1]:
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
