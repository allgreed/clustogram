import json
import sys
import os

from flask import Flask, render_template
from flask_cors import CORS, cross_origin
from jsonschema import validate

from utils import get_json_content

app = Flask('graph')
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
    # wtf why is this set? o.0
    return render_template("index.html", path_to_static=ui_static_content)


if __name__ == "__main__":
    input_data = sys.stdin.read()
    # TODO: guard against this not being set?
    ui_static_content = os.environ["UI_STATIC_CONTENT"]
    print(ui_static_content)
    app.template_folder = ui_static_content
    app.static_folder = os.path.join(ui_static_content)
    app.run(port='8000')
