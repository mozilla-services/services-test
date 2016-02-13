"""
This module uses Fabric API to generate a Firefox Profile by concatenating the
following preferences files:
- ./_utils/prefs.ini
- ./<application>/prefs.ini
- ./<application>/<test_type>/prefs.ini

The profile is then created using the specified name and saved to the ./_temp/
directory.
"""

import os
from fabric.api import local
# TODO: Use configargparse to get args from CLI or use ENV vars?

PATH_PROJECT = os.path.abspath('../')
PATH_TEMP = os.path.join(PATH_PROJECT, '_temp')
FILE_PREFS = 'prefs.ini'

application = 'loop-server'
test_type = 'stack-check'
env = 'stage'
profile = 'BANANAS2'


def prefs_paths(application, test_type, env='stage'):
    path_global = os.path.join(PATH_PROJECT, '_utils', FILE_PREFS)
    path_app_dir = os.path.join(PATH_PROJECT, application)
    path_app = os.path.join(path_app_dir, FILE_PREFS)
    path_app_test_type = os.path.join(path_app_dir, test_type, FILE_PREFS)

    valid_paths = [path_global]

    if os.path.exists(path_app):
        # TODO: Make sure target config file has an {env} section?
        valid_paths.append(path_app + ":" + env)

    if os.path.exists(path_app_test_type):
        # TODO: Make sure target config file has an {env} section?
        valid_paths.append(path_app_test_type + ":" + env)

    return valid_paths

# os.environ['PATH_FIREFOX_PROFILES']

def create_mozprofile(application, test_type, env, profile_dir):
    cmd = ['mozprofile', '--profile={0}'.format(os.path.join(PATH_TEMP, profile_dir))]
    for path in prefs_paths(application, test_type, env):
        cmd.append("--preferences=" + path)

    local(" ".join(cmd))


create_mozprofile(application, test_type, env, profile)
