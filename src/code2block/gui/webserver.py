import json
import os

from flask import Flask, abort

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

@webapp.get("/add_module?module_name=<module_name>")
def add_module(module_name):
    blocks_data = app.generate_blocks(module_name)
    js_path = os.path.join(host_path, "js")
    with open(os.path.join(js_path, f"{module_name}_blocks.js"), "w") as block_file:
        block_file.write(f"{module_name}_block_definitions = ")
        block_file.write(json.dumps(blocks_data["blocks"], default=lambda o: o.__dict__))
    with open(os.path.join(js_path, f"{module_name}_toolbox_data.js"), "w") as toolbox_file:
        toolbox_file.write(f"{module_name}_toolbox_data = ")
        toolbox_file.write(json.dumps(blocks_data["toolbox_category"], default=lambda o: o.__dict__))
    with open(os.path.join(js_path, f"{module_name}_code_generators.js"), "w") as generators_file:
        generators_text = ""
        for generator in blocks_data["code_generators"]:
            generators_text += "\nBlockly.Python['" + generator[
                'block_type'] + "'] = function(block) {\n\tvar code = '" + generator[
                                   'code'] + "';\n\treturn code;\n};\n"
        generators_file.write(generators_text)
    return "Module loaded"


def start_webserver(app_ref):
    global app
    app = app_ref
    webapp.run()
