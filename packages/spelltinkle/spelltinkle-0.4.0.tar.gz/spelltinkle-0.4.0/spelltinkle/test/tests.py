import time

from .selftest import test


@test(args=['asdf'])
def writeas(session):
    yield '^d^k^k12345<enter><home><home>^k^p^p^a^k^p^p^a^k^p^p^p^p.<enter>'
    yield '# hello<enter>'
    yield 'A' * 25 * 1
    yield '<up>^a^b^b<down>^c<page-up>^p'
    yield 'if 1:<enter>a = 1<enter>b = a'
    yield '<enter>^x^w<bs><bs><bs><bs>writeas.txt<enter>'


@test(args=['open2.py'])
def open2(session):
    with open('open2.py', 'w') as fd:
        fd.write('# hello\na = 42\n')
    yield '<home><home>^shello^s <home>^b^b<up>^d'
    yield '^sA<right>^k^x^w'
    yield '<bs>' * len('open2.py')
    yield 'open2b.py<enter>'
    yield '^oopen2.py<enter>^v2^q'


@test()
def mouse(session):
    session.scr.position = (3, 1)
    yield 'a.bc<enter><mouse1-clicked>^d'
    assert session.docs[-1].lines[0] == 'abc'
    session.scr.position = (3, 4)
    yield '<mouse1-clicked>'
    assert session.docs[-1].view.pos == (1, 0)
    yield '1<enter>2<enter><up><up><up><end><down>'
    assert session.docs[-1].view.pos == (1, 1)


@test()
def noend(session):
    with open('noend.py', 'w') as fd:
        fd.write('a = {\n}')
    yield '^onoend.py<enter>'
    assert session.docs[-1].lines[1] == '}'
    yield '^q'


# @test()
def complete_import(session):
    yield 'from collect<tab>'
    assert session.docs[-1].lines[0].endswith('collections')
    yield '.ab<tab>'
    assert session.docs[-1].lines[0].endswith('collections.abc')
    yield ' import Seq<tab>'
    assert session.docs[-1].lines[0].endswith('Sequence')


@test()
def replace(session):
    with open('Replace.py', 'w') as fd:
        fd.write('a = {\n}')
    yield '^oRepl<tab><enter><end><end><enter>aa<enter>aaa<enter>aaaa<enter>'
    yield '<home><home>^fa<right>12<enter>ynyyynn!<down>.'
    yield '<home><home>^f12<right>A<enter>!^w'
    txt = '|'.join(session.docs[-1].lines)
    assert txt == 'A = {|}|aA|AAa|aAAA|.', txt
    yield '^q'


@test(args=['openline.txt:2'], files=[('openline.txt', '1\n2\n')])
def openline(session):
    assert session.docs[-1].view.pos == (1, 0), session.docs[-1].view.pos
    yield '^q'


# @test()
def test7(session):
    yield '({[()]})<home>'
    c = session.docs[-1].color.colors[0]
    assert c[0] // 28 == 3, (c, len(c))
    yield '<end>'
    assert c[0] // 28 == 3, c


@test()
def test8(session):
    yield '1<enter>2<enter>3<enter>'
    yield '<home><home>^k^k<down>^x^k^k<up>^y<bs>^a<bs>'
    assert session.docs[-1].lines[0] == '132'


@test()
def test9(session):
    yield 'abc<enter>'
    yield '123<enter>'
    session.scr.position = (4, 1)
    yield '<mouse1-clicked>'
    session.scr.position = (5, 2)
    yield '<mouse1-released>'
    time.sleep(0.5)
    session.scr.position = (2, 1)
    yield '<mouse2-clicked>'
    assert ''.join(session.doc.lines) == 'c123abc123'


@test()
def test10(session):
    yield 'AAA^rA^r^r'
    pos = session.docs[0].view.pos
    assert pos == (0, 1), pos


@test()
def test11(session):
    yield '^vt^n'
    print(session.docs[-1].lines[:7])
    print(session.docs[-1].view.lines[:7])
    yield '^q'


@test(args=['hmm.py'])
def jedi(session):
    yield 'a11 = 8<enter>'
    yield 'a12 = 8<enter>'
    yield 'a1'
    yield '<tab>'
    x = session.docs[-1].lines[-1]
    assert x == 'a11', session.docs[-1].lines


@test()
def todo(session):
    yield 'abc,def:asdf<enter>'
    yield 'abc:<enter>'
    yield ' hello<enter>'
    yield 'def:hmm<enter>'
    yield '<F5>'


@test()
def write(session):
    yield 'abc'
    with open('abc.123', 'w') as fd:
        fd.write('123')
    yield '^wabc.123<enter><enter>abc.1234<enter>...^w'


@test(files=[('hmmm/grrr/abc.txt', 'hmm')])
def fileinput(session):
    yield '^ohmm<tab><tab><tab><enter>'
    assert session.docs[1].lines[0] == 'hmm'
    yield '^q'


@test()
def rectangle_insert(session):
    yield 'aaa<enter>'
    yield 'a<enter>'
    yield 'aa<enter>'
    yield 'aaa<enter>'
    yield '12^a^k<up><right><ctrl_up><up><up><right>^b^y'
    assert '+'.join(session.docs[0].lines) == 'a12a+a+a12+a12a+'


@test()
def mark_and_copy(session):
    yield 'a1234<left>^u^y'
    assert session.docs[0].lines[0] == 'a1234a1234'


def mail(session):
    yield '^vm^q^q'


def calender(session):
    yield '^vc^q^q'
