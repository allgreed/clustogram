from flask import Flask
from utils import get_json_content

app = Flask('graph')

if __name__ == "__main__":
    content = get_json_content("./src/data.json")
    print(content)


@app.route('/data')
def data_index():
    return get_json_content("./src/data.json")


@app.route('/')
def index():
    return {"Status": "ok"}


