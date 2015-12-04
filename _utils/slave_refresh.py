#!/usr/bin/env python

from firefox_download import FirefoxDownload
from firefox_env_handler import IniHandler
from firefox_install import FirefoxInstall
from firefox_profile_handler import FirefoxProfileHandler
from firefox_uninstall import FirefoxUninstall

# Load our OS-specific INI config file.
os_cfg = IniHandler()
os_cfg.load_os_config("configs")

# Create the ".env" file which will need to be "sourced" from the .bashrc or
# .bashprofile file to get Firefox path ENV vars.
os_cfg.create_env_file()

# Download the latest versions of Firefox.
download = FirefoxDownload(os_cfg)
download.download_all()

# Uninstall all the existing Firefox applications.
uninstall = FirefoxUninstall(os_cfg)
uninstall.uninstall_all()

# Delete the shared Firefox profiles directory.
profile_handler = FirefoxProfileHandler(os_cfg)
profile_handler.delete_all_profiles()

# Install the latest versions of Firefox.
install = FirefoxInstall(os_cfg)
install.install_all()
