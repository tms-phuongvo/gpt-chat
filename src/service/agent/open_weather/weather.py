import requests
import datetime

from langchain_core.tools import tool
from src.utils.constant import WEATHER_HTML


class OpenWeather:
    URL = "https://api.openweathermap.org/data/2.5/weather"

    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_weather(self, lat: float, lon: float) -> dict:
        params = {
            "lat": lat,
            "lon": lon,
            "appid": self.api_key,
        }

        response = requests.get(self.URL, params=params)
        return response.json()

    def convert_markdown(self, weather: dict) -> str:
        return WEATHER_HTML.format(
            city=weather["name"],
            country=weather["sys"]["country"],
            temp=self.__convert_K_to_C(weather["main"]["temp"]),
            feels_like=self.__convert_K_to_C(weather["main"]["feels_like"]),
            humidity=weather["main"]["humidity"],
            pressure=weather["main"]["pressure"],
            visibility=weather["visibility"] // 1000,
            wind_speed=weather["wind"]["speed"],
            wind_direction=weather["wind"]["deg"],
            cloudiness=weather["clouds"]["all"],
            rainfall=(
                weather["rain"]["1h"]
                if "rain" in weather and "1h" in weather["rain"]
                else 0
            ),
            weather_description=weather["weather"][0]["description"],
            sunrise=datetime.datetime.fromtimestamp(weather["sys"]["sunrise"]).strftime(
                "%H:%M"
            ),
            sunset=datetime.datetime.fromtimestamp(weather["sys"]["sunset"]).strftime(
                "%H:%M"
            ),
        )

    def __convert_K_to_C(self, temp: float) -> float:
        return round(temp - 273.15, 2)


@tool
def get_weather_tool():
    """
    When user wants to know about weather for current location.
    """
    return 0.0, 0.0
