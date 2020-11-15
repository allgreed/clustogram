from flask import Flask
from utils import get_json_content

app = Flask('graph')

if __name__ == "__main__":
    content = get_json_content("./src/data.json")
    print(content)


@app.route('/data')
def data_index():
    return get_json_content("./src/data.json")

# TODO: read data from stdin

# TODO: implement CORS for local development (localhost:8080)

# TODO: use real data.json, conforming to schema from contracts
# TODO: use data from stdin <- actually we don't need real data.json once this is implemented

# TODO: serve static content on /

@app.route('/')
def index():
    return {"Status": "ok"}
