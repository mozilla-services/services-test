#!/usr/bin/env python

from firefox_env_handler import IniHandler

import os
import sys


class FirefoxInstall(object):
    def __init__(self, config, archive_dir='temp'):
        self.CACHE_FILE = 'cache.ini'
        self.out_dir = archive_dir
        self.cache_path = os.path.join(self.out_dir, self.CACHE_FILE)
        self.cache = IniHandler(self.cache_path)

        # Do some basic type checking on the `config` attribute.
        if isinstance(config, IniHandler):
            self.config = config

        elif isinstance(config, str):
            self.config = IniHandler()
            self.config.load_os_config(config)

        else:
            sys.exit('FirefoxInstall: Unexpected config data type')

    def install_all(self, force=False):
        IniHandler.banner('INSTALLING FIREFOXES')
        for channel in self.config.sections():
            self.install_channel(channel, force)

    def install_channel(self, channel, force=False):
        was_cached = self.cache.config.getboolean('cached', channel)

        if force or not was_cached:
            if IniHandler.is_linux():
                # TODO: Move to /opt/* and chmod file?
                print(("Installing {0}".format(channel)))

            elif IniHandler.is_windows():
                # TODO: Silent run setup.exe?
                print(("Installing {0}".format(channel)))

            elif IniHandler.is_mac():
                # TODO: Mount the DMG to /Volumes and copy to /Applications?
                print(("Installing {0}".format(channel)))

        else:
            print(("[{0}] was cached, skipping install".format(channel)))


def main():
    ff_install = FirefoxInstall('./configs/')
    ff_install.install_all(True)


if __name__ == '__main__':
    main()
