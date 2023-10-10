import json
import os

from src.code2block.classes.app import App
from src.code2block.gui import webserver

if __name__ == '__main__':
    pylsp_command = ["pylsp", "-v", "--log-file", r"D:\Egyetem\2023_tavasz\Szakdolgozat\Logs\pylsp.log"]
    app = App(pylsp_command)
    app.open_file("D:/Egyetem/2023_tavasz/Szakdolgozat/Workspace/test.py")

    test_module = input("Give me a module name: ")
    blocks_data = app.generate_blocks(test_module)
    root_path = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(root_path, "gui", "js", "blocks.js"), "w") as block_file:
        block_file.write("block_definitions = ")
        block_file.write(json.dumps(blocks_data["blocks"], default=lambda o: o.__dict__))
    with open(os.path.join(root_path, "gui", "js", "toolbox_data.js"), "w") as toolbox_file:
        toolbox_file.write("toolbox_data = ")
        toolbox_file.write(json.dumps(blocks_data["toolbox_category"], default=lambda o: o.__dict__))
    with open(os.path.join(root_path, "gui", "js", "code_generators.js"), "w") as generators_file:
        generators_text = ""
        for generator in blocks_data["code_generators"]:
            generators_text += "\nBlockly.Python['" + generator[
                'block_type'] + "'] = function(block) {\n\tvar code = '" + generator[
                                   'code'] + "';\n\treturn code;\n};\n"
        generators_file.write(generators_text)

    webserver.start_webserver(app)
    app.exit()
