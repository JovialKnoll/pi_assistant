import json
import urllib.parse
import urllib.request
from datetime import datetime

import config


def get_weather(latlong):
    url = 'https://api.openweathermap.org/data/2.5/weather?appid={}&lat={}&lon={}'.format(
        config.KEY_OPENWEATHERMAP,
        latlong[0],
        latlong[1],
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


def get_location():
    url = 'https://ipinfo.io/?token={}'.format(
        config.KEY_IPINFO
    )
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    content = response.read()
    ipinfo_dict = json.loads(content)
    return (
        '{}, {}'.format(
            ipinfo_dict['city'],
            ipinfo_dict['country']
        ),
        ipinfo_dict['timezone'],
    )


def get_time():
    location, time_zone = getLocation()
    time_utc = datetime.now(timezone('UTC'))
    time_here = time_utc.astimezone(timezone(time_zone))
    time_str = time_here.strftime('%I:%M%p')
    return "It is now {}".format(time_str)
