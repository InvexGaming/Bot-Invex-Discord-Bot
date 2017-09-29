import configparser

''' Config import file which can be included to access config values '''

# Parse config
def GetConfig():
    config = configparser.ConfigParser()
    config.sections()
    config.read('config.ini')
    return config