import configparser


config = configparser.ConfigParser(allow_no_value=True)

config.read('manifest.ini')

for key in config['prod']:
    print(key)
