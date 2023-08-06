import os
import sys
import json
import configparser
from configparser import SafeConfigParser

#configuration utilities
class ConfigUtil(object):

    @staticmethod
    def loadConfigFile(config_file_path='', config_ini_path=''):
        config_json = ConfigUtil.loadConfigJson(config_file_path)
        config_ini = ConfigUtil.loadConfigIni(config_ini_path)
        for k, v in config_ini.items():
            if k in config_json:
                config_json[k].update(v)
            else:
                config_json[k] = v
        return config_json

    @staticmethod
    def loadJsonConfig(filename):
        with open(filename, encoding='utf-8') as config_file:
            config = json.load(config_file, encoding='utf-8')
        return config
    
    @staticmethod
    def loadConfigJson(config_file_path=''):
        if config_file_path == '':
            config_file_path = ConfigUtil.config_file_path
        return ConfigUtil.loadJsonConfig(config_file_path)

    #function to handle ini file
    @staticmethod
    def loadIniConfig(filename):
        parser = SafeConfigParser()
        parser.read(filename)
        return ConfigUtil.dumpConfig(parser)

    #function to handle ini file
    @staticmethod
    def loadConfigIni(config_ini_path=''):
        if config_ini_path == '':
            config_ini_path = ConfigUtil.config_ini_path
        return ConfigUtil.loadIniConfig(config_ini_path)

    @staticmethod
    def dumpConfig(parser):
        dictionary = {}
        for section in parser.sections():
            dictionary[section] = {}
            for option in parser.options(section):
                try:
                    dictionary[section][option] = parser.get(section, option, vars=os.environ)
                except configparser.InterpolationMissingOptionError as err:
                    dictionary[section][option] = ''
        return dictionary

