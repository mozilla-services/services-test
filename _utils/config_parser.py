import os
import platform
import ConfigParser

Config = ConfigParser.ConfigParser()
Config.read('path_firefox.ini')

system = platform.system().lower().split('_').pop(0)

env_vars = []

for key in Config.options(system):
    env_vars.append('export %s=%s' % (key.upper(), Config.get(system, key)))

with open('.env', 'w') as f:
    f.write('\n'.join(env_vars))
