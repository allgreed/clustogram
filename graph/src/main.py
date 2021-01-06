import json
import sys
import os

from flask import Flask, send_from_directory
from flask_cors import CORS, cross_origin
from jsonschema import validate

from utils import get_json_content
from produce_graph import produce_graph

app = Flask('graph')
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/data')
@cross_origin()
def data_index():
    my_output = produce_graph(json.loads(input_data))
    validate(
        instance=my_output,
        schema=get_json_content("../contracts/graph-to-ui.json")
    )
    return my_output


@app.route("/<path:filename>")
def index(filename):
    return send_from_directory(ui_static_content, filename)


@app.route("/")
def _index():
    return send_from_directory(ui_static_content, "index.html")


if __name__ == "__main__":
    try:
        input_data = sys.stdin.read()
        ui_static_content = os.environ["UI_STATIC_CONTENT"]
    except KeyError:
        print("Not found the environment variable UI_STATIC_CONTENT")
        sys.exit(1)
    app.static_folder = os.path.join(ui_static_content)
    print(ui_static_content)
    print(app.static_folder)
    app.run(port='8000')
