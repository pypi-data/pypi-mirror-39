import asyncio
import pathlib
from imapclient import IMAPClient
from queue import Queue

from spelltinkle.config import configure


def read_password(host):
    txt = (pathlib.Path.home() / '.spelltinkle' / 'secrets.py').read_text()
    dct = {}
    exec(txt, dct)
    return dct['secrets'][host]


class Server:
    def __init__(self):
        self.config = configure().mail[0]
        self.queue = Queue()

    def connect(self):
        host = self.config['host']
        self.server = IMAPClient(host, ssl=True)
        self.server.login(self.config['user'], read_password(host))

    def run(self, mailbox):
        while True:
            task, arg = self.queue.get()
            if task == 'messages':
                self.messages(arg, mailbox)
            elif task == 'stop':
                return

    def messages(self, folder, mailbox):
        self.server.select_folder(folder)
        messages = self.server.search(['NOT', 'DELETED'])
        loop = asyncio.get_loop()
        loop.call_soon(mailbox.messages, folder, messages)
