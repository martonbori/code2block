import json
from typing import List

from pylspclient import lsp_structs, LspClient
# TODO: Port to sansio-lsp

class TextDocumentContentChangeEvent:
    def __init__(self, range: lsp_structs.Range, rangeLength: int, text: str):
        self.range = range
        self.rangeLength = rangeLength
        self.text = text


class MyLspClient(LspClient):

    def didChange(self, textDocument, contentChanges):
        self.lsp_endpoint.send_notification("textDocument/didChange", textDocument=textDocument, contentChanges=contentChanges)
