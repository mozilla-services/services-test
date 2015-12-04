#!/usr/bin/env python

from firefox_env_handler import IniHandler

import os
import urllib2
import sys


class FirefoxDownload(object):

    def __init__(self, config, out_dir="temp", clean=False):
        """
        TODO:
        """
        # Do some basic type checking on the `config` attribute.
        if isinstance(config, IniHandler):
            self.config = config
        elif isinstance(config, basestring):
            self.config = IniHandler()
            self.config.load_os_config(config)
        else:
            sys.exit("FirefoxDownload: Unexpected config data type")

        self.CACHE_FILE = "cache.ini"
        self.out_dir = out_dir
        self.cache_path = os.path.join(out_dir, self.CACHE_FILE)

        # If `clean` is truthy, delete the current cache folder and then
        # recreate the INI cache file.
        if clean:
            IniHandler.clean_folder(self.out_dir)

        self.create_cache_file()
        self.cache = IniHandler(self.cache_path)

    def create_cache_file(self):
        """
        Ensure the specified output directory and cache INI file exists. If
        the `out_dir` and cache file already exist, this method is a noop.
        """
        # Make sure the `out_dir` exists.
        if not os.path.isdir(self.out_dir):
            os.makedirs(self.out_dir)

        # Create an etags cache INI file, if one doesn't already exist.
        if not os.path.isfile(self.cache_path):
            with open(self.cache_path, "w") as file:
                cache = IniHandler()
                cache.config.add_section("etags")
                cache.config.add_section("cached")
                cache.config.write(file)
                file.close()

    def download_all(self):
        """
        Loop over each channel in the config INI file and download the latest
        build.
        """
        IniHandler.banner("DOWNLOADING FIREFOXES")

        for channel in self.config.sections():
            self.download_channel(channel)

    def download_channel(self, channel):
        """
        Download a specific channel of Firefox (ie: nightly, aurora, beta, ...)
        """
        # Get the full download URL and output filename from the config.
        download_filename = self.config.get(channel, "DOWNLOAD_FILENAME")
        download_url = self.config.get(channel, "DOWNLOAD_URL")
        out_file = os.path.join(self.out_dir, download_filename)

        # Attempt to download the latest version of the Firefox binary for
        # the current channel.
        self.download_file_from_url(download_url, out_file, channel)

    def download_file_from_url(self, download_url, out_file, channel):
        """
        Download the specified channel Firefox build, using an "intelligent"
        cache, using the archive's current `etag` as a unique identifier.
        """
        with open(out_file, "wb") as file:
            try:
                contents = urllib2.urlopen(download_url)
                etag = contents.headers["etag"]
                was_cached = False

                # We found this channel in the cache, but not sure if it is
                # recent.
                if self.cache.config.has_option("etags", channel):
                    # Etags matched, we "probably" have the latest version.
                    if etag == self.cache.get("etags", channel):
                        was_cached = True
                    # Etag cache miss, download latest channel Firefox binary.
                    else:
                        was_cached = False
                # We didn't find this channel in the cache file, download away!
                else:
                    was_cached = False

                # Update the etag cache with the latest etag fingerprint.
                self.cache.set('etags', channel, etag)
                self.cache.set('cached', channel, was_cached)

                if not was_cached:
                    print("Downloading [%s] from %s" % (channel, download_url))
                    file.write(contents.read())
                else:
                    print "[%s] etag was cached, skipping download." % channel

            except urllib2.HTTPError as err:
                # For some reason the download failed. Possibly due to a config
                # mismatch in the INI files. :shrug:
                # TODO: Currently we fail silently here. Fail harder?
                print("\t", err)

            file.close()

        # Rewrite the Etag cache information back into our internal config.
        with open(self.cache_path, "w") as cache:
            self.cache.config.write(cache)
            cache.close()


def main():
    config_path = './configs/'
    ff_dl = FirefoxDownload(config_path)
    ff_dl.download_all()


if __name__ == '__main__':
    main()
