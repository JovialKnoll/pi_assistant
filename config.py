import os
import json

_SRC_DIRECTORY = os.path.dirname(__file__)
_CONFIG_FILE = os.path.join(_SRC_DIRECTORY, 'config.json')
_config = None
with open(_CONFIG_FILE) as file:
    _config = json.load(file)

KEY_IPINFO = _config['key_ipinfo']
KEY_OPENWEATHERMAP = _config['key_openweathermap']
CONFIG_LATLONG_HOME = _config['config_latlong_home'].split(',')
CONFIG_LATLONG_WORK = _config['config_latlong_work'].split(',')

WIDTH = 250
HEIGHT = 122
