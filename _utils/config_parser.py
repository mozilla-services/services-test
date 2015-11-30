#!/usr/bin/env python

import os
import platform
import shutil
import urllib
import ConfigParser

DOWNLOAD_TMP_FOLDER = ".tmp"


def get_os():
    """
    Get the current Operating System.
    """
    return platform.system().lower().split("_").pop(0)


def load_config():
    """
    Load an INI config filed based on operating system.
    """
    os_config = "configs/%s.ini" % (get_os())

    # Fail fast if the input INI config file isn't found for current OS.
    if not os.path.isfile(os_config):
        print("Config file not found for specified OS: %s" % (get_os()))
        exit(1)

    # Load and return the config parser.
    config = ConfigParser.ConfigParser()
    config.read(os_config)
    return config


def download_firefoxes(config):
    """
    Download Firefox archives for all the specified channels.
    """
    header("DOWNLOAD FIREFOXES (%s)" % (get_os()))

    # If the temp folder already exists, forcibly remove it.
    if os.path.isdir(DOWNLOAD_TMP_FOLDER):
        shutil.rmtree(DOWNLOAD_TMP_FOLDER)

    # Create the temp directory before downloading files.
    os.makedirs(DOWNLOAD_TMP_FOLDER)

    # Loop over each section and download the latest OS specific binaries.
    for section in config.sections():
        download_filename = config.get(section, "DOWNLOAD_FILENAME")
        download_url = config.get(section, "DOWNLOAD_URL")
        download_path = os.path.join(DOWNLOAD_TMP_FOLDER, download_filename)
        print "Downloading [%s]... %s" % (section, download_url)
        urllib.urlretrieve(download_url, download_path)


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
    Draw a pretty header.
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
