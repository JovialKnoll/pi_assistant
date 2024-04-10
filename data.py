import json
import urllib.request

import config


def get_weather(lat, long):
    url = 'https://api.openweathermap.org/data/2.5/weather?appid={}&lat={}&lon={}'.format(
        config.KEY_OPENWEATHERMAP,
        lat,
        long,
    )
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    if response.getcode() != 200:
        return None
    content = response.read()
    weather = json.loads(content)
    if weather['cod'] == '404':
        return None
    return weather
