from langchain_core.tools import tool
from lazop_sdk import LazopClient, LazopRequest
import requests

from langchain_core.tools import tool

from src.utils.constant import COIN_HTML


class SearchProduct:

    def __init__(self, app_key: str, app_secret: str, access_token: str):
        self.url = "https://api.lazada.vn/rest"
        self.app_key = app_key
        self.app_secret = app_secret
        self.access_token = access_token

    def search_product(self, search: str) -> dict:
        client = LazopClient(self.url, self.app_key, self.app_secret)
        request = LazopRequest("/products/get", "GET")
        request.add_api_param("filter", "live")
        request.add_api_param("update_before", "2018-01-01T00:00:00+0800")
        request.add_api_param("create_before", "2018-01-01T00:00:00+0800")
        request.add_api_param("offset", "0")
        request.add_api_param("create_after", "2010-01-01T00:00:00+0800")
        request.add_api_param("update_after", "2010-01-01T00:00:00+0800")
        request.add_api_param("limit", "10")
        request.add_api_param("options", "1")
        request.add_api_param("sku_seller_list", '["{}"]'.format(search))
        response = client.execute(request, self.access_token)

        return response.body


@tool
def get_contact_inform():
    """
    When user wants to contact or order something from us.
    """
    return ""


@tool
def search_product(search: str):
    """
    When user wants to search something from our store.
    """
    return ""
