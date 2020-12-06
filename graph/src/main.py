import sys
import json
import os

from flask import Flask
from flask import render_template
from flask_cors import CORS, cross_origin
from jsonschema import validate

from utils import get_json_content

app = Flask('graph', template_folder=os.environ['CLI_STATIC_CONTENT'])
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/data')
@cross_origin()
def data_index():
    my_output = json.loads(input_data)
    validate(
        instance=my_output,
        schema=get_json_content("../contracts/graph-to-ui.json")
    )
    return {'my data json': my_output}


@app.route('/')
def index():
    share = os.environ['CLI_STATIC_CONTENT']
    return render_template("index.html", message=share)


if __name__ == "__main__":
    input_data = sys.stdin.read()
    print(input_data)
    app.run(port='8000')


