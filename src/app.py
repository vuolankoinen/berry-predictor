from http.server import HTTPServer, BaseHTTPRequestHandler
import os
from keras.models import load_model
import pandas as pd

class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'<h1>Berry predictor</h1>')
        self.wfile.write(b'<p>Berry prediction for the next season:<br>At this time, the predicted amount of berries to reach sales in Lapland is...</p>')
        # Lingonberries
        try:
            prediction_text =  '<p>  {:1.1f} tons for <b>lingonberries</b>.</p>'.format(predict('lingonberry-lapland')[0][0])
        except Exception as e:
            prediction_text = '<p>Prediction for lingonberries was unsuccesful:<br>' + str(e) + '</p>'
        self.wfile.write(prediction_text.encode())
        # Blueberries
        try:
            prediction_text = '<p> {:1.1f} tons for <b>blueberries</b>.</p>'.format(predict('blueberry-lapland')[0][0])
        except Exception as e:
            prediction_text = '<p>Prediction for blueberries was unsuccesful:<br>' + str(e) + '</p>'
        self.wfile.write(prediction_text.encode())
        # Cloudberries
        try:
            prediction_text = '<p> {:1.1f} tons for <b>cloudberries</b>.</p>'.format(predict('cloudberry-lapland')[0][0])
        except Exception as e:
            prediction_text = '<p>Prediction for cloudberries was unsuccesful:<br>' + str(e) + '</p>'
        self.wfile.write(prediction_text.encode())

def start_server():
    HTTPServer(('', int(os.environ['PORT'])), Server).serve_forever()

def predict(case):
    net = load_model(os.getcwd() + '/src/nnet/' + case + '.net')
    recent = pd.read_csv(os.getcwd() + '/data/inputs-recent.csv')
    with open(os.getcwd() + '/data/mean-' + case + '.dat') as f:
        mean = float(f.readline())
    rec = pd.DataFrame(columns = range(0, len(recent)))
    rec.loc[0] = list(recent.iloc[:, 1])
    return net.predict(rec)*mean

if __name__ == "__main__":
    start_server()
