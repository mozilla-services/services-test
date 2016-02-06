import os
import fileinput

PATH_PROJECT = os.path.abspath('../') 
PATH_TEMP = 'temp'
FILE_PREFS = 'prefs.ini'

def prefs_paths(application, test_type, env='stage'):
    """concatenate a generic prefs file for testing with a
    prefs file for a specific application and environment"""

    path_global = '{0}/_utils/{1}'.format(PATH_PROJECT, FILE_PREFS)
    file_prefs = '{0}:{1}'.format(FILE_PREFS, env)
    path_app = '{0}/{1}/{2}'.format(PATH_PROJECT, application, file_prefs)
    path_app_test_type = '{0}/{1}/{2}/{3}'.format(
        PATH_PROJECT, application, test_type, file_prefs
    )
    return path_global, path_app, path_app_test_type

application = 'loop-server'
test_type = 'integration'
env = 'stage'
a,b,c = prefs_paths(application, test_type, env)

print(a)
print(b)
print(c)
