from http.server import HTTPServer, BaseHTTPRequestHandler
import os
from keras.models import load_model
import pandas as pd

class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        prediction_text = os.getcwd()
        try:
            net = load_model(os.getcwd() + '/src/nnet/Lingonberry-Lapland.net')
            prediction_text = '<p>Berry prediction:<br>At this time, the predicted amount of lingonberries to reach sales in Lapland is {} tons.</p>'.format(pred_lingonberries()[0][0])
        except Exception as e:
            prediction_text = prediction_text + '<p>File not found at getcwd/src/nnet: ' + str(e) + '</p>'
        self.wfile.write(prediction_text.encode())
        # self.wfile.write(("<p>listdir get:" + str(os.listdir(os.getcwd())) + "</p>").encode())
        # self.wfile.write(("<p>listdir get:" + str(os.listdir(os.getcwd() + '/src')) + "</p>").encode())
        # self.wfile.write(("<p>listdir get:" + str(os.listdir(os.getcwd() + '/src/nnet')) + "</p>").encode())
        # self.wfile.write(('<p>' + os.getcwd() + '</p>').encode())
        # self.wfile.write(("<p>listdir get:" + str(os.listdir(os.getcwd())) + "</p>").encode())

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
