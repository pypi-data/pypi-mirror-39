keynames = {
    '^a': 'home',
    '^c': 'copy',
    '^d': 'delete',
    '^e': 'end',
    '^f': 'replace',
    '^g': 'code_analysis',
    '^h': 'help',
    '^i': 'tab',
    '^k': 'delete_to_end_of_line',
    '^m': 'enter',
    '^n': 'down1',
    '^o': 'open',
    '^p': 'up',
    '^q': 'quit',
    '^r': 'search_backward',
    '^s': 'search_forward',
    '^u': 'mark_word',
    '^v': 'view_files',
    '^w': 'write',
    '^y': 'paste',
    '^z': 'stop',
    '^ ': 'normalize_space',
    'F5': 'refresh',
    'F6': 'spell_check',
    'F7': 'yapf',
    'F8': 'jedi',
    'F9': 'complete',
    'F10': 'format'}

doubles = {
    '½': {'s': 'spell_check',
          'y': 'yapf',
          'j': 'jedi',
          'c': 'complete',
          'f': 'format'},
    '^x': {'^g': 'game',
           '^k': 'delete_to_end_of_line_again',
           '^u': 'undo',
           '^q': 'quit_all',
           '^r': 'redo',
           '^w': 'write_as',
           '^n': ['home', 'enter', 'up', 'tab'],
           '+': 'upper',
           '-': 'lower'},
    '^b': {'^b': 'mark',
           '^y': 'rectangle_insert',
           '^d': 'rectangle_delete',
           '<': 'dedent',
           '>': 'indent'},
    '^t': {'1': 'task_ordered',
           '#': 'task_renumber',
           '^t': 'task_sort'}}

again = {'delete_to_end_of_line'}

repeat = {'home', 'end'}

typos = {'imoprt': 'import'}

aliases = {'np': 'import numpy as np',
           'plt': 'import matplotlib.pyplot as plt',
           'path': 'from pathlib import Path',
           'dd': 'from collections import defaultdict',
           'main': "if __name__ == '__main__':",
           'init': 'def __init__(self):'}
