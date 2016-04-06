#!/usr/bin/env python

from firefox_env_handler import IniHandler
from fabric.api import local

import os
import sys


class FirefoxUninstall(object):
    def __init__(self, config, archive_dir="temp"):
        self.CACHE_FILE = "cache.ini"
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
            sys.exit("FirefoxUninstall: Unexpected config data type")

    def uninstall_all(self, force=False):
        """
        Delete all the Firefox apps (nightly, aurora, beta, general release),
        and then delete the shared profiles directory.
        """
        IniHandler.banner("UNINSTALLING FIREFOXES")

        for channel in self.config.sections():
            self.uninstall_channel(channel, force)

    def uninstall_channel(self, channel, force=False):
        was_cached = self.cache.config.getboolean("cached", channel)

        if force or not was_cached:
            path_firefox_app = self.config.get(channel, "PATH_FIREFOX_APP")
        if not os.path.isdir(path_firefox_app):
            print(('Firefox not found: {0}'.format(path_firefox_app)))
            return

            # If we're on Windows/Cygwin, use the uninstaller.
            if self.config.is_windows():
                local("\"{0}/uninstall/helper.exe\" -ms".format(
                    path_firefox_app))

            # Otherwise just rimraf the Firefox folder.
            else:
                IniHandler.clean_folder(path_firefox_app, False)

        else:
            print(("[%s] was cached, skipping uninstall." % (channel)))


def main():
    config_path = "./configs/"
    ff_uninstall = FirefoxUninstall(config_path)
    ff_uninstall.uninstall_all()

if __name__ == '__main__':
    main()
