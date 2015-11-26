import os
import platform
import ConfigParser

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

    """ fail fast if the input INI file isn't found for current OS. """
    if not os.path.isfile(os_config):
        print("Config file not found for specified OS: %s" % (get_os()))
        exit(1)

    config = ConfigParser.ConfigParser()
    config.read(os_config)
    return config


def download_firefoxes(config):
    """
    Download Firefox archives for all the channels.
    TODO: Do that thing.
    """
    header("DOWNLOAD FIREFOXES")

    WGET_CMD = "wget -O tmp/%s \"https://download.mozilla.org/?product=%s&os=%s\""

    for section in config.sections():
        print WGET_CMD % (
            config.get(section, "INSTALLER_FILENAME"),
            config.get(section, "PRODUCT"),
            config.get(section, "OS")
        )


def create_env_file(config, out_file):
    """
    Generate and save the output environment file so we can source it from
    something like .bashrc or .bashprofile.
    """
    header("CREATE ENV FILE (%s)" % (out_file))

    env_fmt = "export %s=\"%s\""
    env_vars = []

    """
    Generic paths to Sikuli and Firefox profile directories.
    """
    for key in ["PATH_SIKULIX_BIN", "PATH_FIREFOX_PROFILES"]:
        env_vars.append(env_fmt % (key, config.get("DEFAULT", key + "_ENV")))

    """
    Channel specific Firefox binary paths.
    """
    for section in config.sections():
        export_name = "PATH_FIREFOX_APP_" + section.upper()
        firefox_bin = config.get(section, "PATH_FIREFOX_BIN_ENV")
        env_vars.append(env_fmt % (export_name, firefox_bin))

    output = "\n".join(env_vars) + "\n"
    print(output)

    with open(out_file, "w") as env_file:
        env_file.write(output)


def header(str):
    divider = "=" * 60
    print("\n\n%s\n%s\n%s" % (divider, str.upper(), divider))


def main():
    config = load_config()
    download_firefoxes(config)
    create_env_file(config, ".env")


main()
