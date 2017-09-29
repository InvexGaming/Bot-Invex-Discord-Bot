import configparser

''' Config import file which can be included to access config values '''

config = None

# Parse config
def GetConfig():
    global config
    
    # Only read once
    if config is None:
        config = configparser.ConfigParser()
        config.sections()
        config.read('config.ini')
    
    return config