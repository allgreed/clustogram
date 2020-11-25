import sys

from flask import Flask
from flask_cors import CORS, cross_origin
from jsonschema import validate

from utils import get_json_content

app = Flask('graph')
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/data')
@cross_origin()
def data_index():
    my_output = eval(input_data)
    validate(
        instance=my_output,
        schema=get_json_content("../contracts/graph-to-ui.json")
    )
    return {'my data json': my_output}

# TODO: serve static content on /
@app.route('/')
def index():
    return {"Status": "ok"}


if __name__ == "__main__":
    input_data = sys.stdin.read()
    print(input_data)
    app.run(port='8000')


