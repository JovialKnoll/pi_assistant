import os
import json

_SRC_DIRECTORY = os.path.dirname(__file__)
_CONFIG_FILE = os.path.join(_SRC_DIRECTORY, 'config.json')
_config = None
with open(_CONFIG_FILE) as file:
    _config = json.load(file)

KEY_IPINFO = _config['key_ipinfo']
KEY_OPENWEATHERMAP = _config['key_openweathermap']
CONFIG_CITY_HOME = _config['config_city_home']
CONFIG_CITY_WORK = _config['config_city_work']

WIDTH = 250
HEIGHT = 122
