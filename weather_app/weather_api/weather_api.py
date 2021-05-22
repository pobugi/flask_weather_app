import requests


def weather_request(city_name):
    url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=05443b3ba2b770a860712cc4afb3a43e"

    return requests.get(url.format(city_name)).json()


