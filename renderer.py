from PIL import Image, ImageChops, ImageDraw, ImageFont

import config
import data


# drawing vars
small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
medium_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
large_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
icon_font = ImageFont.truetype("./meteocons.ttf", 48)
ICON_MAP = {
    "01d": "B",
    "01n": "C",
    "02d": "H",
    "02n": "I",
    "03d": "N",
    "03n": "N",
    "04d": "Y",
    "04n": "Y",
    "09d": "Q",
    "09n": "Q",
    "10d": "R",
    "10n": "R",
    "11d": "Z",
    "11n": "Z",
    "13d": "W",
    "13n": "W",
    "50d": "J",
    "50n": "K",
}
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


def _get_blank_image():
    return Image.new("RGB", (config.WIDTH, config.HEIGHT), color=WHITE)


def _get_celsius(kelvin):
    return kelvin - 273.15


def _get_fahrenheit(celsius):
    return (celsius * 9/5) + 32


_width_for_temp_c = large_font.getsize("000°C")[0]


def _display_weather(weather, label):
    temp_c = _get_celsius(weather["main"]["temp"])
    temp_f = _get_fahrenheit(temp_c)
    feels_like_c = _get_celsius(weather["main"]["feels_like"])
    feels_like_f = _get_fahrenheit(feels_like_c)

    image = _get_blank_image()
    draw = ImageDraw.Draw(image)

    draw.text((0, 0), label, font=medium_font, fill=BLACK)
    (label_font_width, label_font_height) = medium_font.getsize(label)
    
    description = weather["weather"][0]["description"]
    description = description[0].upper() + description[1:]
    (font_width, font_height) = small_font.getsize(description)
    xy = (0, config.HEIGHT - font_height)
    draw.text(xy, description, font=small_font, fill=BLACK)

    main = weather["weather"][0]["main"]
    (font_width, font_height) = large_font.getsize(main)
    xy = (0, xy[1] - font_height)
    draw.text(xy, main, font=large_font, fill=BLACK)

    weather_icon = ICON_MAP[weather["weather"][0]["icon"]]
    (font_width, font_height) = icon_font.getsize(weather_icon)
    xy = (0, label_font_height + (xy[1] - label_font_height) // 2 - font_height // 2)
    draw.text(xy, weather_icon, font=icon_font, fill=BLACK)

    temperature_c = "%d°C" % round(temp_c)
    (font_width, font_height) = large_font.getsize(temperature_c)
    xy = (config.WIDTH - font_width, 0)
    draw.text(xy, temperature_c, font=large_font, fill=BLACK)
    old_font_height = font_height
    temperature_f = "%d°F" % round(temp_f)
    (font_width, font_height) = large_font.getsize(temperature_f)
    xy = (config.WIDTH - font_width - _width_for_temp_c, 0)
    draw.text(xy, temperature_f, font=large_font, fill=BLACK)
    old_font_height = max(old_font_height, font_height)

    feels_like = "feels like"
    (font_width, font_height) = small_font.getsize(feels_like)
    xy = (config.WIDTH - font_width, xy[1] + old_font_height)
    draw.text(xy, feels_like, font=small_font, fill=BLACK)
    old_font_height = font_height

    y = xy[1] + old_font_height
    temperature_c = "%d°C" % round(feels_like_c)
    (font_width, font_height) = large_font.getsize(temperature_c)
    xy = (config.WIDTH - font_width, y)
    draw.text(xy, temperature_c, font=large_font, fill=BLACK)
    temperature_f = "%d°F" % round(feels_like_f)
    (font_width, font_height) = large_font.getsize(temperature_f)
    xy = (config.WIDTH - font_width - _width_for_temp_c, y)
    draw.text(xy, temperature_f, font=large_font, fill=BLACK)

    return image


def _get_weather_display(location, label):
    weather = data.get_weather(location)
    if not weather:
        return None
    return _display_weather(weather, label)


def _get_home_weather():
    return _get_weather_display(config.CONFIG_CITY_HOME, "Home")


def _get_work_weather():
    return _get_weather_display(config.CONFIG_CITY_WORK, "Work")


def _get_page_2():
    image = _get_blank_image()
    draw = ImageDraw.Draw(image)
    draw.text(
        (20, 20), "page 2", font=medium_font, fill=BLACK,
    )
    draw.text(
        (70, 70), "page 2", font=medium_font, fill=BLACK,
    )
    draw.text(
        (120, 120), "page 2", font=medium_font, fill=BLACK,
    )
    return image


_pages = (
    (_get_home_weather, 10 * 60),
    (_get_work_weather, 10 * 60),
    (_get_page_2, 10 * 60),
)


page_count = len(_pages)


def get_page(page_index, current_image):
    new_image = _pages[page_index][0]()
    delay = _pages[page_index][1]
    if not current_image \
    or (new_image and ImageChops.difference(current_image, new_image).getbbox()):
        return new_image, delay
    return None, delay
