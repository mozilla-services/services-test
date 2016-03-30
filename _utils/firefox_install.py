#!/usr/bin/env python

from firefox_env_handler import IniHandler
from fabric.api import local

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
        filename = self.config.get(channel, 'DOWNLOAD_FILENAME')
        install_dir = self.config.get(channel, 'PATH_FIREFOX_APP')
        installer = os.path.join('.', self.out_dir, filename)

        if force or not was_cached:
            print(('Installing {0}'.format(channel)))

            if IniHandler.is_linux():
                # TODO: Move to /opt/* and chmod file?
                # `tar -jxf firefox-beta.tar.gz -C
                # ./beta --strip-components=1`?
                local('tar -jxf {0} && mv firefox {1}'.format(
                    installer, install_dir))

            elif IniHandler.is_windows():
                local('{0} -ms'.format(installer))

                if channel == 'beta':
                    # Since Beta and General Release channels install
                    # to the same directory,
                    # install Beta first then rename the directory.
                    gr_install_dir = self.config.get('gr', 'PATH_FIREFOX_APP')
                    local('mv "{0}" "{1}"'.format(
                        gr_install_dir, install_dir))

            elif IniHandler.is_mac():
                # TODO: Mount the DMG to /Volumes and copy to /Applications?
                print('Do something...')

        else:
            print(('[{0}] was cached, skipping install.'.format(channel)))

        local('"{0}" --version # {1}'.format(
            self.config.get(channel, 'PATH_FIREFOX_BIN_ENV'), channel))


def main():
    ff_install = FirefoxInstall('./configs/')
    ff_install.install_all(True)


if __name__ == '__main__':
    main()
