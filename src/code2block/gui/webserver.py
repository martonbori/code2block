import json
import os

from flask import Flask, abort, request

from src.code2block.classes.app import App

webapp = Flask(__name__)
webapp.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

app: App
host_path = os.path.dirname(os.path.realpath(__file__))


@webapp.route("/")
def get_index_page():
    with open(os.path.join(host_path, 'html', 'index.html.j2'), "r") as index_file:
        return index_file.read()


@webapp.route("/js/<path:subpath>")
def get_js_file(subpath):
    try:
        js_file = open(os.path.join(host_path, "js", subpath), 'rb').read()
    except IOError as error:
        abort(404, "File not Found")
    else:
        return js_file

@webapp.post("/add_module")
def add_module():
    module_name = request.form["module_name"]
    ret = {}
    blocks_data = app.generate_blocks(module_name)
    ret["blocks"] = blocks_data["blocks"]
    ret["category"] = blocks_data["toolbox_category"]
    ret["generators"] = blocks_data["code_generators"]
    return json.dumps(ret, default=lambda o: o.__dict__)


def start_webserver(app_ref):
    global app
    app = app_ref
    webapp.run()
