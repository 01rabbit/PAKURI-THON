from configparser import ConfigParser
import os


def config(filename, section):
    # create a parser
    parser = ConfigParser()
    # read config file
    filepath=os.path.join(os.path.dirname(__file__), filename)
    parser.read(filepath, encoding='utf-8')
    result = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            result[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return result

def db_conf():
    return config('config.ini','postgresql')

def webssh_conf():
    return config('config.ini','webssh')

def empire_conf():
    return config('config.ini','empire')

def matter_conf():
    return config('config.ini','mattermost')

if __name__ == '__main__':
    config()
