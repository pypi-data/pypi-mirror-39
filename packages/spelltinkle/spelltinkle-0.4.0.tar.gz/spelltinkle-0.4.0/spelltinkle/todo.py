from collections import defaultdict


def refresh(doc):
    lines = {}
    id = 0
    indents = []
    data = defaultdict(list)
    sortafter = {}
    newlines = []
    for j, line in enumerate(doc.lines):
        if line.startswith(':'):
            sortafter = {tag: -i
                         for i, tag in enumerate(line[1:].split(','))}
            newlines.append(line)
            continue
        L = line.lstrip()
        n = len(line) - len(L)
        L = L.rstrip()
        if L == '':
            continue
        indents = [(m, tags) for m, tags in indents if m < n]
        if L.endswith(':'):
            assert ' ' not in L, L
            indents.append((n, L[:-1].split(',')))
        else:
            if ':' in L:
                tags, txt = L.split(':', 1)
                tags = tags.split(',')
                if all(tag.islower() and tag.isalnum() for tag in tags):
                    L = txt.lstrip()
                else:
                    tags = []
            else:
                tags = []
            for n, itags in indents:
                tags += itags
            lines[id] = (tags, L)
            for tag in tags:
                data[tag].append(id)
            id += 1
    newlines += sort(data, lines, '', sortafter)
    assert sum(1 for line in newlines
               if line[0] == ' ' and not line.endswith(':')) == id
    r = doc.view.r
    doc.change(0, 0, len(doc.lines) - 1, 0, newlines + [''])
    doc.changes = 42
    doc.view.message = 'Items: ' + str(id)
    doc.view.move(r)


def sort(data, lines, indent, sortafter={}):
    result = []
    while data:
        tag = max((sortafter.get(tag, -999), len(ids), tag)
                  for tag, ids in data.items())[2]
        ids = data.pop(tag)
        newdata = defaultdict(list)
        here = []
        for id in ids:
            if id not in lines:
                continue
            tags, line = lines[id]
            tags.remove(tag)
            for t in tags:
                newdata[t].append(id)
            if len(tags) == 0:
                del lines[id]
                here.append(line)
        here += sort(newdata, lines, indent)
        if here:
            result.append(indent + tag + ':')
            for line in here:
                result.append(indent + ' ' + line)
    return result
