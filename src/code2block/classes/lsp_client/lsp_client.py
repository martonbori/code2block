import contextlib
import string
import subprocess
from typing import Optional, List

import sansio_lsp_client as sansio_lsp
from sansio_lsp_client import WorkspaceFolder, TextDocumentPosition, CompletionContext, JSONDict, TextDocumentItem, \
    VersionedTextDocumentIdentifier, TextDocumentContentChangeEvent, ClientState, TextDocumentIdentifier, \
    FormattingOptions, Range, TextDocumentSaveReason

from src.code2block.classes.lsp_client.io_server import IOThreadedServer

METHOD_COMPLETION = "completion"
METHOD_HOVER = "hover"
METHOD_SIG_HELP = "signatureHelp"
METHOD_DEFINITION = "definition"
METHOD_REFERENCES = "references"
METHOD_IMPLEMENTATION = "implementation"
METHOD_DECLARATION = "declaration"
METHOD_TYPEDEF = "typeDefinition"
METHOD_DOC_SYMBOLS = "documentSymbol"
METHOD_FORMAT_DOC = "formatting"
METHOD_FORMAT_SEL = "rangeFormatting"
RESPONSE_TYPES = {
    METHOD_COMPLETION: sansio_lsp.Completion,
    METHOD_HOVER: sansio_lsp.Hover,
    METHOD_SIG_HELP: sansio_lsp.SignatureHelp,
    METHOD_DEFINITION: sansio_lsp.Definition,
    METHOD_REFERENCES: sansio_lsp.References,
    METHOD_IMPLEMENTATION: sansio_lsp.Implementation,
    METHOD_DECLARATION: sansio_lsp.Declaration,
    METHOD_TYPEDEF: sansio_lsp.TypeDefinition,
    METHOD_DOC_SYMBOLS: sansio_lsp.MDocumentSymbols,
    METHOD_FORMAT_DOC: sansio_lsp.DocumentFormatting,
    METHOD_FORMAT_SEL: sansio_lsp.DocumentFormatting,
}


class LspClient:

    def __init__(self,
                 lsp_server_command: List[string],
                 process_id: Optional[int] = None,
                 root_uri: Optional[str] = None,
                 workspace_folders: Optional[List[WorkspaceFolder]] = None,
                 trace: str = "off",
                 ):

        self.response_messages = {}
        self.sansio_lsp_client = sansio_lsp.Client(process_id, root_uri, workspace_folders, trace)
        with self.start_lsp_server(lsp_server_command) as io_server:
            self.io_server = io_server
            self.io_server.wait_for_message_of_type(sansio_lsp.Initialized)

    @contextlib.contextmanager
    def start_lsp_server(self, command: List[string]) -> IOThreadedServer:
        process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        io_server = IOThreadedServer(process.stdin, process.stdout, self.sansio_lsp_client)
        try:
            yield io_server
        except Exception as e:
            # Prevent freezing tests
            process.kill()
            raise e

        # io_server.exit_cleanly()

    def exit(self) -> None:
        self.io_server.exit_cleanly()

    def cancel_last_request(self) -> None:
        self.sansio_lsp_client.cancel_last_request()

    def did_open(self, text_document: TextDocumentItem) -> None:
        self.sansio_lsp_client.did_open(text_document)

    def did_change(self,
                   text_document: VersionedTextDocumentIdentifier,
                   content_changes: List[TextDocumentContentChangeEvent],
                   ) -> None:
        self.sansio_lsp_client.did_change(text_document, content_changes)

    def will_save(
            self, text_document: TextDocumentIdentifier, reason: TextDocumentSaveReason
    ) -> None:
        self.sansio_lsp_client.will_save(text_document, reason)

    def will_save_wait_until(
            self, text_document: TextDocumentIdentifier, reason: TextDocumentSaveReason
    ) -> None:
        self.sansio_lsp_client.will_save_wait_until(text_document, reason)

    def did_save(
            self, text_document: TextDocumentIdentifier, text: Optional[str] = None
    ) -> None:
        self.sansio_lsp_client.did_save(text_document, text)

    def did_close(self, text_document: TextDocumentIdentifier) -> None:
        self.sansio_lsp_client.did_close(text_document)

    def did_change_workspace_folders(
            self, added: List[WorkspaceFolder], removed: List[WorkspaceFolder]
    ) -> None:
        self.did_change_workspace_folders(added, removed)

    def completion(
        self,
        text_document_position: TextDocumentPosition,
        context: Optional[CompletionContext] = None,
    ) -> sansio_lsp.Completion:
        req_id = self.sansio_lsp_client.completion(text_document_position, context)
        response = self.io_server.wait_for_message_of_type(sansio_lsp.Completion)
        assert not hasattr(response, "message_id") or response.message_id == req_id
        return response

    def hover(self, text_document_position: TextDocumentPosition) -> sansio_lsp.Hover:
        req_id = self.sansio_lsp_client.hover(text_document_position)
        response = self.io_server.wait_for_message_of_type(sansio_lsp.Hover)
        assert not hasattr(response, "message_id") or response.message_id == req_id
        return response

    def signatureHelp(self, text_document_position: TextDocumentPosition) -> sansio_lsp.SignatureHelp:
        req_id = self.sansio_lsp_client.signatureHelp(text_document_position)
        response = self.io_server.wait_for_message_of_type(sansio_lsp.SignatureHelp)
        assert not hasattr(response, "message_id") or response.message_id == req_id
        return response

    def definition(self, text_document_position: TextDocumentPosition) -> sansio_lsp.Definition:
        req_id = self.sansio_lsp_client.definition(text_document_position)
        response = self.io_server.wait_for_message_of_type(sansio_lsp.Definition)
        assert not hasattr(response, "message_id") or response.message_id == req_id
        return response

    def declaration(self, text_document_position: TextDocumentPosition) -> sansio_lsp.Declaration:
        req_id = self.sansio_lsp_client.declaration(text_document_position)
        response = self.io_server.wait_for_message_of_type(sansio_lsp.Declaration)
        assert not hasattr(response, "message_id") or response.message_id == req_id
        return response

    def typeDefinition(self, text_document_position: TextDocumentPosition) -> sansio_lsp.TypeDefinition:
        req_id = self.sansio_lsp_client.typeDefinition(text_document_position)
        response = self.io_server.wait_for_message_of_type(sansio_lsp.TypeDefinition)
        assert not hasattr(response, "message_id") or response.message_id == req_id
        return response

    def references(self, text_document_position: TextDocumentPosition) -> sansio_lsp.References:
        req_id = self.sansio_lsp_client.references(text_document_position)
        response = self.io_server.wait_for_message_of_type(sansio_lsp.References)
        assert not hasattr(response, "message_id") or response.message_id == req_id
        return response

    def implementation(self, text_document_position: TextDocumentPosition) -> sansio_lsp.Implementation:
        req_id = self.sansio_lsp_client.implementation(text_document_position)
        response = self.io_server.wait_for_message_of_type(sansio_lsp.Implementation)
        assert not hasattr(response, "message_id") or response.message_id == req_id
        return response

    def workspace_symbol(self, query: str = "") -> sansio_lsp.MWorkspaceSymbols:
        req_id = self.sansio_lsp_client.workspace_symbol(query)
        response = self.io_server.wait_for_message_of_type(sansio_lsp.MWorkspaceSymbols)
        assert not hasattr(response, "message_id") or response.message_id == req_id
        return response

    def documentSymbol(self, text_document: TextDocumentIdentifier) -> sansio_lsp.MDocumentSymbols:
        req_id = self.sansio_lsp_client.documentSymbol(text_document)
        response = self.io_server.wait_for_message_of_type(sansio_lsp.MDocumentSymbols)
        assert not hasattr(response, "message_id") or response.message_id == req_id
        return response

    def formatting(
        self, text_document: TextDocumentIdentifier, options: FormattingOptions
    ) -> sansio_lsp.DocumentFormatting:
        req_id = self.sansio_lsp_client.formatting(text_document, options)
        response = self.io_server.wait_for_message_of_type(sansio_lsp.DocumentFormatting)
        assert not hasattr(response, "message_id") or response.message_id == req_id
        return response

    def rangeFormatting(
        self,
        text_document: TextDocumentIdentifier,
        range: Range,
        options: FormattingOptions,
    ) -> sansio_lsp.DocumentFormatting:
        req_id = self.sansio_lsp_client.rangeFormatting(text_document, range, options)
        response = self.io_server.wait_for_message_of_type(sansio_lsp.DocumentFormatting)
        assert not hasattr(response, "message_id") or response.message_id == req_id
        return response


