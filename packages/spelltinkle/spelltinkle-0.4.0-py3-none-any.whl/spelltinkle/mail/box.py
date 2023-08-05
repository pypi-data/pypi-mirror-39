class MailBox:
    def __init__(self):

        self.server = Server()
        self.server.connect()
        thread = threading.Thread(target=self.server.run)
        thread.start()

        self.mails = {}
        self.folders = []
        self.observers = []

    def remember(self, observer):
        self.observers.append(observer)

    def forget(self, observer):
        self.observers.delete(observer)

    def messages(self, folder, messages):
        self.folders[...] = ...
        self.notify()

    def notify(self):
        for observer in self.observers:
            observer.notify()

    def get_message(self, id):
        pass
