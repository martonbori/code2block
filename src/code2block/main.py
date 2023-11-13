import json
import os

from src.code2block.classes.app import App
from src.code2block.gui import webserver

if __name__ == '__main__':
    pylsp_command = ["pylsp", "-v", "--log-file", r"C:/Users/Marci/Documents/Egyetem/2023_tavasz/Szakdolgozat/Logs/pylsp.log"]
    app = App(pylsp_command)
    app.open_file("C:/Users/Marci/Documents/Egyetem/2023_tavasz/Szakdolgozat/Workspace/test.py")

    webserver.start_webserver(app)
    app.exit()
