#!/usr/bin/env python

import os
import configargparse
from subprocess import Popen


def _parse_args():
    """Parses out args for CLI"""
    parser = configargparse.ArgumentParser(
        description='CLI tool for running Push integration tests')
    parser.add_argument('-b', '--binary',
                        help='Path to Firefox binary')

    args = parser.parse_args()
    return args, parser


def main():
    args, parser = _parse_args()
    path_nightly = args.binary

    if not path_nightly:
        if os.environ.get('PATH_FIREFOX_APP_NIGHTLY'):
            path_nightly = os.environ.get('PATH_FIREFOX_APP_NIGHTLY')
        else:
            exit('Unable to locate Firefox binary. Specify using `--binary` arg.')

    proc_express = Popen(['node', 'app/server.js'])
    proc_test = Popen(['python', 'runtests.py', 'test_push.py',
                       '--binary', path_nightly])

    proc_test.wait()

    proc_express.terminate()

if __name__ == '__main__':
    main()
