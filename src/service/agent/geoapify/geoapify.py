from langchain_core.tools import tool
import requests


class GeoPlaces:
    URL = "https://api.geoapify.com/v2/places"

    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_place_restaurant(
        self, lat: float, lon: float, radius: int, **kwargs
    ) -> dict:
        params = {
            "categories": "catering.restaurant,commercial.food_and_drink",
            "filter": f"circle:{lon},{lat},{radius * 1000}",
            "bias": f"proximity:{lon},{lat}",
            "apiKey": self.api_key,
            "limit": 20,
        }
        print(params)
        response = requests.get(self.URL, params=params)
        print(response.json())
        return response.json()


@tool
def get_restaurant_tool(meals: str, radius: int):
    """
    When the user asks what they want to eat, they either want to find a restaurant or suggest a dish.
    User need select meals and radius for restaurant type and place

    Args:
    meals: breakfast, lunch or dinner required user input
    radius: Radius around current location in km required user input
    """
    return ""
