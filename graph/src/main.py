import sys

from flask import Flask
from flask_cors import CORS, cross_origin

from utils import get_json_content


app = Flask('graph')
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/data')
@cross_origin()
def data_index():
    return get_json_content("./src/data.json")

# TODO: use real data.json, conforming to schema from contracts

# TODO: serve static content on /

# TODO: use data from stdin <- actually we don't need real data.json once this is implemented


@app.route('/')
def index():
    return {"Status": "ok"}

if __name__ == "__main__":
    ble = sys.stdin.read()
    print(ble)
    app.run()
