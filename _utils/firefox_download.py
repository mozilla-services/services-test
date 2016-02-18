"""
Module to download OS-specific versions of Firefox:
1. General Release (gr)
2. Beta (beta)
3. Developer Edition (aurora)
4. Nightly (nightly)
"""

from firefox_env_handler import IniHandler
from mozdownload import FactoryScraper


CONFIG_CHANNELS = 'configs/channels.ini'

try:
    import configparser  # Python 3
except:
    import ConfigParser as configparser  # Python 2

config = configparser.ConfigParser()
config.read(CONFIG_CHANNELS)
env = IniHandler()
env.load_os_config('configs')


def set_channel(channel):
    ch_version = config.get(channel, 'version')
    ch_type = config.get(channel, 'type')
    ch_branch = config.get(channel, 'branch')
    return ch_version, ch_type, ch_branch


def download(channel):
    print('USING CHANNEL: {0}'.format(channel))
    v, t, b = set_channel(channel)
    download_filename = env.get(channel, 'DOWNLOAD_FILENAME')
    scraper = FactoryScraper(
        t,
        version=v,
        branch=b,
        destination='_temp/{0}'.format(download_filename)
    )
    scraper.download()


def main():
    for channel in config.sections():
        download(channel)


if __name__ == '__main__':
    main()
