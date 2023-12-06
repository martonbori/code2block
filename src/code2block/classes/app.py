import os
import pathlib
from typing import List, Tuple

from sansio_lsp_client import WorkspaceFolder, TextDocumentItem, VersionedTextDocumentIdentifier, \
    TextDocumentContentChangeEvent, TextDocumentIdentifier, TextDocumentPosition, Position, SignatureHelp, \
    SymbolInformation, DocumentSymbol, CompletionItem, SignatureInformation

from src.code2block.classes import block_factory
from src.code2block.classes.lsp_client.lsp_client import LspClient


class App:
    document: TextDocumentItem
    document_path: os.PathLike

    def __init__(self, lsp_server_command):
        self.lsp_client = LspClient(
            lsp_server_command=lsp_server_command,
            process_id=os.getpid(),
            root_uri="file:///D:/Egyetem/2023_tavasz/Szakdolgozat/Workspace",
            workspace_folders=[
                WorkspaceFolder(uri="file://D:/Egyetem/2023_tavasz/Szakdolgozat/Workspace", name="test")],
            trace="off"
        )

    def open_file(self, file_path):
        file_name, file_ext = os.path.splitext(file_path)
        self.document_path = file_path
        language_id = ""
        if file_ext == ".py":
            language_id = "python"
        else:
            raise NotImplementedError(f"Language not implemented ({file_ext})")

        with open(file_path, "r") as file:
            text = file.read()
            self.document = TextDocumentItem(
                uri=pathlib.Path(file_path).as_uri(),
                languageId=language_id,
                version=0,
                text=text
            )
            self.lsp_client.did_open(self.document)

    def update_file(self):
        #with open(self.document_path, "w") as file:
        #    file.write(self.document.text)

        self.document.version += 1
        versioned_id = VersionedTextDocumentIdentifier(
            uri=self.document.uri,
            version=self.document.version
        )
        content_change = TextDocumentContentChangeEvent(
            text=self.document.text
        )
        self.lsp_client.did_change(text_document=versioned_id, content_changes=[content_change])

    def document_symbols(self) -> List[SymbolInformation] | List[DocumentSymbol] | None:
        doc_id = TextDocumentIdentifier(uri=self.document.uri)
        document_symbols = self.lsp_client.documentSymbol(text_document=doc_id)
        return document_symbols.result

    def signature_help(self, line, character) -> SignatureHelp:
        text_document_position = TextDocumentPosition(
            textDocument=TextDocumentIdentifier(uri=self.document.uri),
            position=Position(line=1, character=character)
        )
        signatures = self.lsp_client.signatureHelp(text_document_position)
        return signatures

    def completion_request(self, line, character) -> List[CompletionItem]:
        text_document_position = TextDocumentPosition(
            textDocument=TextDocumentIdentifier(uri=self.document.uri),
            position=Position(line=line, character=character)
        )
        completion_event = self.lsp_client.completion(text_document_position)
        completion_list = completion_event.completion_list.items
        return completion_list

    def find_symbols_rec(self, root_symbol, found_symbols=None) -> List[str]:
        if found_symbols is None:
            found_symbols = []
        if root_symbol in found_symbols:
            return found_symbols
        self.document.text += f"\n{root_symbol}."
        line_count = len(self.document.text.split('\n'))
        self.update_file()
        completion_items = self.completion_request(line_count, len(root_symbol + "."))
        found_symbols.extend([item.label for item in completion_items])
        self.find_symbols_rec(f"{root_symbol}.{completion_items.pop().label}")

    def find_symbols(self, root_symbol) -> List[CompletionItem]:
        col = 0
        if root_symbol:
            self.document.text += f"\n{root_symbol}."
            col = len(root_symbol + ".")
        else:
            self.document.text += f"\n"
        line_count = len(self.document.text.split('\n'))
        self.update_file()
        return self.completion_request(line_count-1, col)

    def get_signature_data(self, module_name, method) -> List[SignatureInformation] | None:
        signature_data = self.signature_help(module_name, method)
        if not signature_data:
            return None
        return signature_data.signatures

    def find_signatures(self, module_name, symbol_labels):
        signature_data = {}
        for idx, label in enumerate(symbol_labels):
            print(f"Get signature data [{idx + 1}/{len(symbol_labels)}] ({label})")
            import_text = f"import {module_name}"
            method_text = f"{module_name}.{label}"
            index = method_text.find("(")
            if index == -1:
                method_text += "("
                index = method_text.find("(")
            self.document.text = f"{import_text}\n{method_text}"
            self.update_file()
            signatures = self.signature_help(line=1, character=index+1).signatures
            if not signatures:
                continue
            signature_data[label] = signatures
        return signature_data

    def discover_module_api(self, module_name):
        # import module
        if module_name:
            self.document.text = f"import {module_name}"
            self.update_file()

        # Find module symbols
        completion_list = self.find_symbols(module_name)

        # Remove private items
        completion_list = \
            [item for item in completion_list if not item.label.startswith("_")]
        print(f"Found {len(completion_list)} symbols")

        # Find signatures
        symbol_labels = [item.label for item in completion_list]
        signature_data = self.find_signatures(module_name, symbol_labels)

        return completion_list, signature_data

    def generate_blocks(self, module_name) -> dict:
        completion_list, signature_data = self.discover_module_api(module_name)

        return block_factory.generate_blocks(module_name=module_name,
                                             completion_list=completion_list,
                                             signature_data=signature_data)


    def exit(self):
        self.lsp_client.exit()
