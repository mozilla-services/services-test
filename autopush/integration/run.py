#!/usr/bin/env python
import time
from subprocess import Popen


def main():
    proc_express = Popen(['node', 'app/server.js'])
    proc_test = Popen(['python', 'runtests.py', 'test_push.py','--binary', '/Applications/FirefoxBETA.app/Contents/MacOS/firefox'])

    time.sleep(40)
    proc_express.terminate()
    proc_test.terminate()

    print('hell');
if __name__ == '__main__':
    print('hell');
    main()
