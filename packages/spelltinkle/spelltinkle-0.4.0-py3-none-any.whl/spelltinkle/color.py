import threading
import subprocess

import pygments.lexers
import pygments.token
import pygments.util
from pygments.formatters.terminal import TERMINAL_COLORS
from pygments.token import Error, Token

RGB = {
    'fuchsia': (255, 0, 255),
    'darkgray': (169, 169, 169),
    'red': (255, 0, 0),
    'green': (0, 128, 0),
    'turquoise': (64, 224, 208),
    'black': (0, 0, 0),
    'lightgray': (211, 211, 211),
    'blue': (0, 0, 255),
    'brown': (165, 42, 42)}

token2color = {Token: 0}
colors = {'black': 0}
highlight_codes = ['black']
for token in TERMINAL_COLORS:
    name = TERMINAL_COLORS[token][1]
    if name:
        color = colors.get(name)
        if color is None:
            color = len(colors)
            colors[name] = color
            highlight_codes.append(name)
        token2color[token] = color

ERROR = token2color[Error]


class NoColor:
    def __init__(self):
        self.colors = [bytearray(200)]
        self.report = []

    def stop(self):
        pass

    def update(self, c1, r1, c2, r2, lines):
        pass

    def run(self, loop):
        pass

    def probe(self, r, c):
        return 0


class Color(NoColor):
    def __init__(self, doc):
        NoColor.__init__(self)
        self.doc = doc
        self.r = None
        self._stop = None
        self.thread = None
        self.athread = None
        self.lexer = None

    def probe(self, r, c):
        try:
            return self.colors[r][c]
        except IndexError:
            return 0

    def stop(self):
        self._stop = True
        if self.thread:
            self.thread.join()
        if self.athread:
            self.athread.cancel()
            try:
                self.athread.join()
            except RuntimeError:
                pass

    def update(self, c1, r1, c2, r2, lines):
        if c1 != c2 or r1 != r2:
            start = self.colors[r1][:c1]
            end = self.colors[r2][c2:]
            if r1 == r2:
                self.colors[r1] = start + end
            else:
                self.colors[r1] = start
                del self.colors[r1 + 1:r2 + 1]
                self.colors[r1].extend(end)
        if lines != ['']:
            start = self.colors[r1][:c1]
            end = self.colors[r1][c1:]
            self.colors[r1] = start + bytearray(len(lines[0]))
            self.colors[r1 + 1:r1 + 1] = [bytearray(len(line))
                                          for line in lines[1:]]
            self.colors[r1 + len(lines) - 1].extend(end)

    def run(self, loop):
        if self.lexer is None:
            try:
                self.lexer = pygments.lexers.get_lexer_for_filename(
                    self.doc.name, stripnl=False)
            except pygments.util.ClassNotFound:
                self.lexer = False
            else:
                name = self.lexer.name
                self.doc.mode = name

        self._stop = False
        if self.lexer:
            self.thread = threading.Thread(target=self.target, args=[loop])
            self.thread.start()

        self.athread = threading.Timer(2.0, self.analyse, [loop])
        self.athread.start()

    def target(self, loop):
        try:
            self.paint()
        except IndentationError:
            pass

        loop.call_soon_threadsafe(self.doc.session.draw_colors)

    def analyse(self, loop):
        self.report = []
        try:
            self.flake8()
        except Exception as e:
            self.doc.view.message = 'flake8!!!'
            self.doc.log(e)
        if loop.is_running():
            loop.call_soon_threadsafe(self.doc.session.draw_colors)

    def paint(self):
        text = '\n'.join(self.doc.lines)
        r = 0
        c = 0
        for token, s in pygments.lex(text, self.lexer):
            if self._stop:
                break
            color = token2color.get(token)
            while color is None:
                token = token[:-1]
                color = token2color.get(token)

            lines = s.split('\n')
            for i, line in enumerate(lines):
                n = len(line)
                for m in range(n):
                    self.colors[r][c + m] = color
                if i == len(lines) - 1:
                    break
                r += 1
                c = 0
            c += n

    def flake8(self):
        if self.doc.path is None or not self.doc.path.name.endswith('.py'):
            return

        p = subprocess.Popen(['flake8', '--ignore=E129,E741,W293,W504', '-'],
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             universal_newlines=True)
        for line in self.doc.lines[:-1]:
            if self._stop:
                return
            print(line, file=p.stdin)
        output = p.communicate()[0]
        if p.returncode == 0:
            return

        for line in output.splitlines():
            if self._stop:
                return
            pos, line = line.split(' ', 1)
            r, c = (int(n) - 1 for n in pos.split(':')[1:3])
            if (line.startswith('E226') and
                self.doc.lines[r][c:c + 2] == '**'):
                continue
            self.colors[r][c] = ERROR
            self.report.append(((r, c), line))
