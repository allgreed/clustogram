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
    content = get_json_content(os.path.join(ui_static_content, "fake_graph.json"))
    print(content)
    my_output = content
    validate(
        instance=my_output,
        schema=get_json_content("../contracts/graph-to-ui.json")
    )
    return {'my data json': my_output}


@app.route('/')
def index():
    return render_template("index.html", path_to_static=ui_static_content)


if __name__ == "__main__":
    ui_static_content = sys.argv[1]
    app.template_folder = ui_static_content
    app.static_folder = os.path.join(ui_static_content, "static")
    app.run(port='8000')


