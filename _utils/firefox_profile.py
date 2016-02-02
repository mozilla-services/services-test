import os
import fileinput

PATH_PROJECT = os.path.abspath('../') 

def write_prefs_file(application, env='stage', dir_tmp='temp'): 
    """concatenate a generic prefs file for testing with a
    prefs file for a specific application and environment"""

    path_pref_app = '{0}/{1}/prefs/{2}.js'.format(PATH_PROJECT, application, env)
    path_pref_any = '{0}/_utils/prefs/any_env.js'.format(PATH_PROJECT)
    filenames = [ path_pref_any, path_pref_app ]
    outfile = '{0}/_utils/{1}/prefs.js'.format(PATH_PROJECT, dir_tmp)

    with open(outfile, 'w') as file_prefs:
        for line in fileinput.input(filenames):
            file_prefs.write(line)

env = 'stage'
application = 'loop-server'
write_prefs_file(application, env)
