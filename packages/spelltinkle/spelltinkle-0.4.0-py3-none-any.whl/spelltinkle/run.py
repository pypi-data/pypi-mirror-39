import argparse
import subprocess
import sys
from importlib.util import find_spec
from typing import List

from spelltinkle.config import configure
from spelltinkle.i18n import set_language
from spelltinkle.session import Session
from spelltinkle.screen import Screen
from spelltinkle.utils import find_files


def run(arguments: List[str] = None):
    parser = argparse.ArgumentParser()
    add = parser.add_argument
    add('files', nargs='*')
    add('-w', '--new-window', action='store_true')
    add('-u', '--user')
    add('-m', '--module', action='append', default=[])
    add('-S', '--self-test', action='store_true')
    add('-D', '--debug', action='store_true')
    add('-L', '--language')
    add('-g', '--git', action='store_true')
    add('-0', '--dry-run', action='store_true')
    add('-f', '--find', action='append', default=[])
    add('-s', '--select')
    args = parser.parse_args(arguments)

    set_language(args.language)

    if args.new_window:
        for option in ['-w', '--new-window']:
            if option in sys.argv:
                sys.argv.remove(option)
                break
        else:
            for i, option in enumerate(sys.argv):
                if option.startswith('-w'):
                    sys.argv[i] = '-' + option[2:]
                    break
            else:
                assert False, sys.argv  # should not happen
        subprocess.check_call(['gnome-terminal',
                               '--geometry',
                               '84x40',
                               '--'] + sys.argv)
        return

    if args.self_test:
        from .test.selftest import run_tests
        return run_tests(args.files)

    for module in args.module:
        spec = find_spec(module)
        assert spec is not None
        args.files.append(spec.origin)

    if args.git:
        out = subprocess.check_output(['git',
                                       'status',
                                       '--porcelain'],
                                      universal_newlines=True)
        for line in out.splitlines():
            status, filename = line.split()
            if status == 'M':
                args.files.append(filename)

    if args.user:
        config = configure()
        args.files.append(config.user_files[args.user])

    for x in args.find:
        args.files.extend(find_files(x))

    if args.dry_run:
        for file in args.files:
            print(file)
        return

    if args.select:
        args.files = eval('args.files[{}]'.format(args.select))
        if isinstance(args.files, str):
            args.files = [args.files]

    scr = Screen()
    session = Session(args.files, scr)
    session.run()
    scr.stop()


if __name__ == '__main__':
    run()
