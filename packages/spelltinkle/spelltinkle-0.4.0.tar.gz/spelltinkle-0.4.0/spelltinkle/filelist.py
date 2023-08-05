import os.path as op

from spelltinkle.document import Document


class FileList(Document):
    def __init__(self):
        Document.__init__(self)
        self.name = '[list]'

    def set_session(self, session):
        Document.set_session(self, session)
        self.change(0, 0, 0, 0, [doc.name
                                 for doc in session.docs[::-1]] +
                    ['[TASKS]', '[EMAIL]', '[CALENDER]', '[IRC]', ''])
        self.view.move(2, 0)
        "save Saveall quit/del/bs enter copy open esc"

    def insert_character(self, c):
        if c.isdigit():
            i = int(c)
            if 0 < i < len(self.session.docs):
                return self.choose(i)
            else:
                c = 'teci'[i - len(self.session.docs)]
        if c == 't':
            from spelltinkle.text import TextDocument
            self.session.docs.pop()
            doc = TextDocument(self.session)
            tasks = op.expanduser('~/.spelltinkle/tasks.txt')
            doc.read(tasks)
            return doc
        if c == 'c':
            from spelltinkle.calender import CalenderDocument
            self.session.docs.pop()
            return CalenderDocument()
        if c == 'm':
            from spelltinkle.mail import MailDocument
            self.session.docs.pop()
            return MailDocument()

    def choose(self, i):
        self.session.docs.pop()
        return self.session.docs.pop(-i)

    def enter(self):
        return self.choose(self.view.r + 1)

    def esc(self):
        return self.choose(1)

    def view_files(self):
        return self.insert_character('2')
