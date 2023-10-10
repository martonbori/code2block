import json
import pprint
import queue
import re
import threading
import time

from sansio_lsp_client import ShowMessageRequest, WorkDoneProgressCreate, RegisterCapabilityRequest, \
    ConfigurationRequest, WorkspaceFolders, WorkspaceFolder, ClientState, Shutdown, Client


class IOThreadedServer:
    """
    Gathers all messages received from server - to handle random-order-messages
    that are not a response to a request.
    """

    def __init__(self, pipe_in, pipe_out, lsp_client: Client):
        self.lsp_client = lsp_client
        self.msgs = []

        self._pout = pipe_out
        self._pin = pipe_in

        self._read_q = queue.Queue()
        self._send_q = queue.Queue()

        self.reader_thread = threading.Thread(
            target=self._read_loop, name="lsp-reader", daemon=True
        )
        self.writer_thread = threading.Thread(
            target=self._send_loop, name="lsp-writer", daemon=True
        )

        self.reader_thread.start()
        self.writer_thread.start()

        self.exception = None

    # threaded
    def _read_loop(self):
        try:
            while True:
                data = self._pout.read(1)
                if data == b"":
                    break

                self._read_q.put(data)
        except Exception as ex:
            self.exception = ex
        self._send_q.put_nowait(None)  # stop send loop

    # threaded
    def _send_loop(self):
        try:
            while True:
                chunk = self._send_q.get()
                if chunk is None:
                    break

                self._pin.write(chunk)
                self._pin.flush()
        except Exception as ex:
            self.exception = ex

    def _queue_data_to_send(self):
        send_buf = self.lsp_client.send()
        if send_buf:
            self._send_q.put(send_buf)

    def _read_data_received(self):
        while not self._read_q.empty():
            data = self._read_q.get()
            events = self.lsp_client.recv(data)
            for ev in events:
                self.msgs.append(ev)
                self._try_default_reply(ev)

    def _try_default_reply(self, msg):
        if isinstance(
            msg,
            (
                    ShowMessageRequest,
                    WorkDoneProgressCreate,
                    RegisterCapabilityRequest,
                    ConfigurationRequest,
            ),
        ):
            msg.reply()

        elif isinstance(msg, WorkspaceFolders):
            msg.reply([WorkspaceFolder(uri=self.lsp_client.root_uri, name="Root")])

        else:
            #print(f"Can't autoreply: {type(msg)}")
            pass
    def wait_for_message_of_type(self, type_, timeout=5):
        end_time = time.monotonic() + timeout
        while time.monotonic() < end_time:
            self._queue_data_to_send()
            self._read_data_received()

            # raise thread's exception if have any
            if self.exception:
                raise self.exception

            for msg in self.msgs:
                if isinstance(msg, type_):
                    self.msgs.remove(msg)
                    return msg

            time.sleep(0.2)

        raise Exception(
            f"Didn't receive {type_} in time; have: " + pprint.pformat(self.msgs)
        )

    def exit_cleanly(self):
        # Not necessarily error, gopls sends logging messages for example
        #        if self.msgs:
        #            print(
        #                "* unprocessed messages: " + pprint.pformat(self.msgs)
        #            )

        assert self.lsp_client.state == ClientState.NORMAL
        self.lsp_client.shutdown()
        self.wait_for_message_of_type(Shutdown)
        self.lsp_client.exit()
        self._queue_data_to_send()
        self._read_data_received()


