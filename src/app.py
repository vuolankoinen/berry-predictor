from http.server import HTTPServer, BaseHTTPRequestHandler
import os
from keras.models import load_model
import pandas as pd

class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        try:
            prediction_text = '<p>Berry prediction for the next season:<br>At this time, the predicted amount of lingonberries to reach sales in Lapland is {:1.1f} tons.</p>'.format(predict('Lingonberry-Lapland')[0][0])
        except Exception as e:
            prediction_text = '<p>Prediction was unsuccesful:<br>' + str(e) + '</p>'
        self.wfile.write(prediction_text.encode())

def start_server():
    HTTPServer(('', int(os.environ['PORT'])), Server).serve_forever()

def predict(case):
    net = load_model(os.getcwd() + '/src/nnet/' + case + '.net')
    recent = pd.read_csv(os.getcwd() + '/data/recent.csv')
    with open(os.getcwd() + '/data/mean-' + case + '.dat') as f:
        mean = float(f.readline())
    rec = pd.DataFrame(columns = range(0, len(recent)))
    rec.loc[0] = list(recent.iloc[:, 1])
    return net.predict(rec * mean)

if __name__ == "__main__":
    start_server()
