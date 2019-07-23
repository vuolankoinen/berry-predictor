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
            prediction_text = prediction_test + '<p>File not found at ../src/nnet/</p>'
        try:
            net = load_model('./nnet/Lingonberry-Lapland.net')
        except:
            prediction_text = prediction_text + '<p>File not found at ./nnet/</p>'
        try:
            net = load_model(os.getcwd() + '/src/nnet/Lingonberry-Lapland.net')
            prediction_text = prediction_text + '<p>File found!</p>'
        except Exception as e:
            prediction_text = prediction_text + '<p>File not found at getcwd/src/nnet:' + str(e) + '</p>'
        self.wfile.write(prediction_text.encode())
        self.wfile.write(("<p>listdir get:" + str(os.listdir(os.getcwd())) + "</p>").encode())
        self.wfile.write(("<p>listdir get:" + str(os.listdir(os.getcwd() + '/src')) + "</p>").encode())
        self.wfile.write(("<p>listdir get:" + str(os.listdir(os.getcwd() + '/src/nnet')) + "</p>").encode())
        os.chdir('./src')
        self.wfile.write(('<p>' + os.getcwd() + '</p>').encode())
        # self.wfile.write(list_dirs().encode())
        self.wfile.write(("<p>listdir .: " + str(os.listdir('.')) + "</p>").encode())
        self.wfile.write(("<p>listdir ..:" + str(os.listdir('..')) + "</p>").encode())
        self.wfile.write(("<p>listdir get:" + str(os.listdir(os.getcwd())) + "</p>").encode())

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
