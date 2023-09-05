import json
import os
import threading
import subprocess
import pylspclient
from pylspclient.lsp_structs import TextDocumentItem, Range, Position

from block_factory import Block, BlockArg
from my_lsp_client import MyLspClient, TextDocumentContentChangeEvent


test_file_path = "D:/Egyetem/2023_tavasz/Szakdolgozat/Workspace/test.py"
test_file_uri = f"file://{test_file_path}"
test_file_version = 0
test_file_line_cnt = 0
test_document = TextDocumentItem(uri=test_file_uri, languageId="python", text="", version=test_file_version)


class ReadPipe(threading.Thread):
    def __init__(self, pipe):
        threading.Thread.__init__(self)
        self.pipe = pipe

    def run(self):
        line = self.pipe.readline().decode('utf-8')
        while line:
            print(f"ERROR {line}")
            line = self.pipe.readline().decode('utf-8')


p = subprocess.Popen(
    ["python", "-u", "-m", "pylsp", "-v", "--log-file", r"D:\Egyetem\2023_tavasz\Szakdolgozat\Logs\pylsp.log"],
    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
jsonrpc_endpoint = pylspclient.JsonRpcEndpoint(stdin=p.stdin, stdout=p.stdout,
                                               logger=lambda *args: print("CLIENT JSONRPC: ", args))
lsp_endpoint = pylspclient.LspEndpoint(jsonrpc_endpoint, logger=lambda *args: print("CLIENT LSP: ", args),
                                       default_callback=lambda text: print(f"SERVER: {text}\n"))
client = MyLspClient(lsp_endpoint=lsp_endpoint)
read_pipe = ReadPipe(p.stderr)
read_pipe.start()


def initialize():
    print(client.initialize(processId=os.getpid(),
                                  rootPath="",
                                  rootUri="file://D:/Egyetem/2023_tavasz/Szakdolgozat/Workspace",
                                  initializationOptions=None,
                                  capabilities={},
                                  # capabilities={"textDocument": {"codeAction": {"dynamicRegistration": True}, "codeLens": {"dynamicRegistration": True}, "colorProvider": {"dynamicRegistration": True}, "completion": {"completionItem": {"commitCharactersSupport": True, "documentationFormat": ["markdown", "plaintext"], "snippetSupport": True}, "completionItemKind": {"valueSet": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]}, "contextSupport": True, "dynamicRegistration": True}, "definition": {"dynamicRegistration": True}, "documentHighlight": {"dynamicRegistration": True}, "documentLink": {"dynamicRegistration": True}, "documentSymbol": {"dynamicRegistration": True, "symbolKind": {"valueSet": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26]}}, "formatting": {"dynamicRegistration": True}, "hover": {"contentFormat": ["markdown", "plaintext"], "dynamicRegistration": True}, "implementation": {"dynamicRegistration": True}, "onTypeFormatting": {"dynamicRegistration": True}, "publishDiagnostics": {"relatedInformation": True}, "rangeFormatting": {"dynamicRegistration": True}, "references": {"dynamicRegistration": True}, "rename": {"dynamicRegistration": True}, "signatureHelp": {"dynamicRegistration": True, "signatureInformation": {"documentationFormat": ["markdown", "plaintext"]}}, "synchronization": {"didSave": True, "dynamicRegistration": True, "willSave": True, "willSaveWaitUntil": True}, "typeDefinition": {"dynamicRegistration": True}}, "workspace": {"applyEdit": True, "configuration": True, "didChangeConfiguration": {"dynamicRegistration": True}, "didChangeWatchedFiles": {"dynamicRegistration": True}, "executeCommand": {"dynamicRegistration": True}, "symbol": {"dynamicRegistration": True, "symbolKind": {"valueSet": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26]}}, "workspaceEdit": {"documentChanges": True}, "workspaceFolders": True}},
                                  workspaceFolders=[
                                      {"name": "test", "uri": "file://D:/Egyetem/2023_tavasz/Szakdolgozat/Workspace"}],
                                  trace="off"))
    print(client.initialized())
    print()


def open_file():
    with open(test_file_path, "w") as file:
        client.didOpen(textDocument=test_document)


def update_file():
    with open(test_file_path, "w") as file:
        file.write(test_document.text)

    global test_file_version
    test_file_version += 1
    client.didChange(textDocument={"uri": test_file_uri}, contentChanges=[{"text": test_document.text}])


def document_symbol_request():
    client.documentSymbol(textDocument={"uri": test_file_uri})


def signature_help_request(module_name, method):
    import_text = f"import {module_name}"
    method_text = f"{module_name}.{method}"
    test_document.text = f"{import_text}\n{method_text}"
    update_file()
    index = method_text.find("(")
    if index == -1:
        return None
    return client.signatureHelp(textDocument={"uri": test_file_uri}, position=Position(1, index + 1))


def completion_request(line, character):
    return client.lsp_endpoint.call_method("textDocument/completion", textDocument={"uri": test_file_uri}, position=Position(line, character))

def get_completion_items(line, character):
    completion_items = []
    completion_result = completion_request(line, character)
    {
        "type"
    }
    for item in completion_result['items']:
        completion_items.append(item['label'])
    return completion_items


def find_symbols_rec(root_symbol, found_symbols=[]):
    if root_symbol in found_symbols:
        return found_symbols
    global test_file_line_cnt
    test_document.text += f"\n{root_symbol}."
    test_file_line_cnt += 1
    update_file()
    completion_items = get_completion_items(test_file_line_cnt, len(root_symbol + "."))
    found_symbols.extend(completion_items)
    find_symbols_rec(f"{root_symbol}.{completion_items.pop()}")

def find_symbols(root_symbol):
    global test_file_line_cnt
    test_document.text += f"\n{root_symbol}."
    test_file_line_cnt += 1
    update_file()
    return get_completion_items(test_file_line_cnt, len(root_symbol + "."))


def get_signature_data(module_name, method):
    signature_data = signature_help_request(module_name, method)
    if not signature_data:
        return
    return signature_data.signatures[0]

def generate_blocks(module_name):
    """ Find symbols in module """
    test_document.text = f"import {module_name}"
    update_file()
    symbols = find_symbols(module_name)

    """ Generate blocks from symbols """
    toolbox_category = {
        "kind": "category",
        "name": module_name,
        "contents": []
    }
    blocks = []
    code_generators = []
    for symbol in symbols:
        signature_data = get_signature_data(module_name, symbol)
        if not signature_data:
            continue
        print(signature_data)
        args = []
        for param in signature_data.parameters:
            args.append(BlockArg(
                type="input_value",
                name=param.label,
                check=None))
        message = symbol
        for i in range(len(args)):
            message += f" %{i+1}"
        label = signature_data.label
        type_name = f"{module_name}_{symbol}".replace('(','_').replace(')','_').replace(' ','_').replace(',','_')
        block = Block(
            type=type_name,
            message0=message,
            args0=args,
            colour=160,
            previousStatement=None,
            nextStatement=None,
            tooltip=label)
        blocks.append(block)
        toolbox_category["contents"].append({"kind": "block", "type": type_name})
        code_generators.append({
            "block_type": type_name,
            "code": label
        })
    return blocks, toolbox_category, code_generators


if __name__ == '__main__':
    initialize()
    open_file()

    #test_module = input("Give me a module name")
    test_module = "random"
    blocks, toolbox_elements, generators = generate_blocks(test_module)

    with open(r"D:\Egyetem\2023_tavasz\Szakdolgozat\repos\project\blocks.js", "w") as block_file:
        block_file.write("block_definitions = ")
        block_file.write(json.dumps(blocks, default=lambda o:o.__dict__))
    with open(r"D:\Egyetem\2023_tavasz\Szakdolgozat\repos\project\toolbox_data.js", "w") as toolbox_file:
        toolbox_file.write("toolbox_data = ")
        toolbox_file.write(json.dumps(toolbox_elements, default=lambda o: o.__dict__))
    with open(r"D:\Egyetem\2023_tavasz\Szakdolgozat\repos\project\code_generators.js", "w") as generators_file:
        generators_text = ""
        for generator in generators:
            generators_text += "\nBlockly.Python['" + generator['block_type'] + "'] = function(block) {\n\tvar code = '"+ generator['code'] +"';\n\treturn code;\n};\n"
        generators_file.write(generators_text)

    #document_symbol_request()
    #signature_help_request()
