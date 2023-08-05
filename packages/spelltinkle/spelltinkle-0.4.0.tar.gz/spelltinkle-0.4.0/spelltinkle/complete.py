import re
from threading import Thread
from typing import List


def complete(word: str, words: List[str]) -> str:
    if not words:
        return word
    if len(words) == 1:
        return words[0]
    n = len(word)
    if len(words[0]) == n:
        return word
    x = words[0][n]
    for w in words[1:]:
        if len(w) == n or w[n] != x:
            break
    else:
        return complete(word + x, words)
    return word


def complete_word(doc):
    # Find the word we are looking for:
    r, c = doc.view.pos
    line = doc.lines[r]
    match = re.search('[a-zA-Z]\w*$', line[:c])
    if not match:
        return
    word = line[match.start():match.end()]

    # Look for possible completions in document:
    n = len(word)
    regex = re.compile(r'\b' + word + '\w*')
    words = set()
    for R, line in enumerate(doc.lines):
        for match in regex.finditer(line):
            c1, c2 = match.span()
            if R != r or c1 != c - n:
                words.add(line[c1:c2])
    newword = complete(word, list(words))
    if newword != word:
        doc.change(r, c, r, c, [newword[n:]])


class Completion:
    def __init__(self):
        self.thread = None
        self._stop = True
        self.completions = None
        self.text_lines: List[str] = []
        self.active = False
        self.line_number = 0

    def run(self, doc, r: int, c: int, loop) -> None:
        if doc.path is None or not doc.path.name.endswith('.py'):
            return

        self._stop = False
        if self.thread:
            self.thread.join()
        self.thread = Thread(target=self.jedi, args=[doc, r, c, loop])
        self.thread.start()

    def stop(self):
        self.completions = None
        self._stop = True
        if self.thread:
            self.thread.join()

    def jedi(self, doc, r, c, loop):
        from jedi import settings, Script

        if settings.case_insensitive_completion:
            settings.case_insensitive_completion = False
            settings.add_bracket_after_function = True

        try:
            s = Script('\n'.join(doc.lines), r + 1, c + 1, '')
            self.completions = s.completions()
        except Exception:
            return
        if self.completions:
            loop.call_soon_threadsafe(self.done, doc)

    def done(self, doc):
        if not self._stop and self.completions:
            names = []
            types = []
            for comp in self.completions:
                try:
                    names.append(comp.name_with_symbols)
                    types.append(comp.type)
                except Exception:
                    self.text_lines = []
                    return
            self.offset = len(comp.name_with_symbols) - len(comp.complete)
            L1 = max(len(name) for name in names)
            L2 = max(len(type) for type in types)
            self.text_lines = ['{:{}} {:>{}}'.format(name, L1, type, L2)
                               for name, type in zip(names, types)]
            self.active = True
            self.line_number = 0
            doc.session.draw_colors()

    def down(self):
        if self.line_number < len(self.text_lines) - 1:
            self.line_number += 1

    def lines(self, w, h, x, y):
        if not self.active or not self.text_lines:
            return 0, 0, 0, 0, 0, []

        a = len(self.text_lines[0])
        b = len(self.text_lines)
        if b > h - y - 1:
            # above
            y1 = max(0, y - b)
            y2 = y
        else:
            y1 = y + 1
            y2 = min(h - 1, y1 + b)
        x1 = x - self.offset
        x2 = x1 + a
        if x2 > w:
            x1 -= x2 - w
            x2 = w
        return (x1, x2, y1, y2,
                self.line_number, self.text_lines[:y2 - y1])

    def word(self):
        return self.text_lines[0].split()[self.line_number][self.offset:]
