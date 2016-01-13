#!/usr/bin/env python

from firefox_env_handler import IniHandler

import os
import sys


class FirefoxUninstall(object):
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
            sys.exit('FirefoxUninstall: Unexpected config data type')

    def uninstall_all(self, force=False):
        """
        Delete all the Firefox apps (nightly, aurora, beta, general release),
        and then delete the shared profiles directory.
        """
        IniHandler.banner('UNINSTALLING FIREFOXES')

        for channel in self.config.sections():
            self.uninstall_channel(channel, force)

    def uninstall_channel(self, channel, force=False):
        was_cached = self.cache.config.getboolean('cached', channel)

        if force or not was_cached:
            path_firefox_app = self.config.get(channel, 'PATH_FIREFOX_APP')
            # If we're on Windows/Cygwin, use the uninstaller.
            if self.config.is_windows():
                print(("{0}/uninstall/helper.exe -ms".format(path_firefox_app)))

            # Otherwise just rimraf the Firefox folder.
            else:
                IniHandler.clean_folder(path_firefox_app)

        else:
            print(("[{0}] was cached, skipping uninstall.".format(channel)))


def main():
    config_path = './configs/'
    FirefoxUninstall(config_path)


if __name__ == '__main__':
    main()
