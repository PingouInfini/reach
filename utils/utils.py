import configparser
import os

config = configparser.RawConfigParser()
config.read('properties.config')

def get_directory_from_property(section, parameter):
    directory = config.get(section, parameter)
    if not directory.endswith('/'):
        directory += '/'

    if not os.path.exists(directory):
        os.makedirs(directory)

    return directory

def get_boolean_from_property(section, parameter):
    return config[section].getboolean(parameter)