#!/usr/bin/env python

import os
import platform
import shutil
import urllib2
import ConfigParser

DOWNLOAD_TMP_FOLDER = ".tmp"


def get_os():
    """
    Get the current Operating System.
    """
    return platform.system().lower().split("_").pop(0)


def load_config(file=get_os()):
    """
    Load an INI config filed based on operating system.
    """
    os_config = "configs/%s.ini" % (file)

    # Fail fast if the input INI config file isn't found for current OS.
    if not os.path.isfile(os_config):
        print("Config file not found for specified OS: %s" % (file))
        exit(1)

    # Load and return the config parser.
    config = ConfigParser.ConfigParser()
    config.read(os_config)
    return config


def download_firefoxes(config, tmp_folder=DOWNLOAD_TMP_FOLDER):
    """
    Download Firefox archives for all the specified channels.
    """
    header("DOWNLOAD FIREFOXES (%s)" % (get_os()))

    # Delete and recreate the temp folder if necessary.
    clean_tmp(tmp_folder)

    # Loop over each section and download the latest OS specific binaries.
    for section in config.sections():
        download_filename = config.get(section, "DOWNLOAD_FILENAME")
        download_url = config.get(section, "DOWNLOAD_URL")
        out_file = os.path.join(tmp_folder, download_filename)

        print("Downloading [%s]... %s" % (section, download_url))
        download_file_from_url(download_url, out_file)


def download_file_from_url(download_url, out_file):
    """
    Download a remote file and save it locally.
    """
    with open(out_file, "wb") as f:
        try:
            contents = urllib2.urlopen(download_url)
            f.write(contents.read())
        except urllib2.HTTPError as err:
            # TODO: Do we need to fail harder here if we're unable to download
            # the specified file? Currently it will silently fail and proceed.
            print("\t", err)

        f.close()


def clean_tmp(tmp_folder):
    """
    rm -rf everything!
    """
    # If the specified folder already exists, forcibly remove it.
    if os.path.isdir(tmp_folder):
        shutil.rmtree(tmp_folder)

    # Create the specified directory before downloading files.
    os.makedirs(tmp_folder)


def create_env_file(config, out_file):
    """
    Generate and save the output environment file so we can source it from
    something like .bashrc or .bashprofile.
    """
    header("CREATE ENV FILE (%s)" % (out_file))

    env_fmt = "export %s=\"%s\""
    env_vars = []

    # Generic paths to Sikuli and Firefox profile directories.
    for key in ["PATH_SIKULIX_BIN", "PATH_FIREFOX_PROFILES"]:
        env_vars.append(env_fmt % (key, config.get("DEFAULT", key + "_ENV")))

    # Channel specific Firefox binary paths.
    for section in config.sections():
        export_name = "PATH_FIREFOX_APP_" + section.upper()
        firefox_bin = config.get(section, "PATH_FIREFOX_BIN_ENV")
        env_vars.append(env_fmt % (export_name, firefox_bin))

    output = "\n".join(env_vars) + "\n"
    print(output)

    with open(out_file, "w") as env_file:
        env_file.write(output)


def header(str):
    """
    Draw a pretty header for easier debugging.
    """
    divider = "=" * 60
    print("\n\n%s\n%s\n%s" % (divider, str, divider))


def main():
    """
    Do all the things!
    """
    config = load_config()
    download_firefoxes(config)
    create_env_file(config, ".env")


main()
