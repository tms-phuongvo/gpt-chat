import requests

from langchain_core.tools import tool

from src.utils.constant import COIN_HTML


class CoinMarketCap:
    URL = "https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest"

    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_crypto_currency(self, symbol: str) -> dict:
        params = {
            "symbol": symbol,
        }
        headers = {"X-CMC_PRO_API_KEY": self.api_key, "Accept": "application/json"}
        response = requests.get(self.URL, params=params, headers=headers)
        return response.json()

    def convert_markdown(self, token: dict) -> str:
        id = token["id"]
        name = token["name"]
        symbol = token["symbol"]
        slug = token["slug"]
        is_active = "Yes" if token["is_active"] else "No"
        is_fiat = "Yes" if token["is_fiat"] else "No"
        date_added = token["date_added"]
        cmc_rank = token["cmc_rank"]
        last_updated = token["last_updated"]
        circulating_supply = (
            f"{token['circulating_supply']:,}"
            if token["circulating_supply"] is not None
            else "N/A"
        )
        total_supply = (
            f"{token['total_supply']:,}" if token["total_supply"] is not None else "N/A"
        )
        max_supply = (
            f"{token['max_supply']:,}" if token["max_supply"] is not None else "N/A"
        )
        price = f"${token['quote']['USD']['price']:,}"

        volume_24h = (
            f"${token['quote']['USD']['volume_24h']:,}"
            if token["quote"]["USD"]["volume_24h"] is not None
            else "N/A"
        )
        volume_change_24h = f"${token['quote']['USD']['volume_change_24h'] * 100:.2f}"
        percent_change_1h = f"{token['quote']['USD']['percent_change_1h']:.2f}"
        percent_change_24h = f"{token['quote']['USD']['percent_change_24h']:.2f}"
        percent_change_7d = f"{token['quote']['USD']['percent_change_7d']:.2f}"
        percent_change_30d = f"{token['quote']['USD']['percent_change_30d']:.2f}"
        market_cap = (
            f"${token['quote']['USD']['market_cap']:,}"
            if token["quote"]["USD"]["market_cap"] is not None
            else "N/A"
        )
        market_cap_dominance = token["quote"]["USD"]["market_cap_dominance"]
        fully_diluted_market_cap = (
            f"${token['quote']['USD']['fully_diluted_market_cap']:,}"
            if token["quote"]["USD"]["fully_diluted_market_cap"] is not None
            else "N/A"
        )

        tags = [tag["slug"] for tag in list(token["tags"])]
        tagString = ", ".join(tags) if len(tags) > 0 else "None"
        num_market_pairs = token["num_market_pairs"]
        return COIN_HTML.format(
            id=id,
            name=name,
            symbol=symbol,
            slug=slug,
            is_active=is_active,
            is_fiat=is_fiat,
            date_added=date_added,
            cmc_rank=cmc_rank,
            last_updated=last_updated,
            circulating_supply=circulating_supply,
            total_supply=total_supply,
            max_supply=max_supply,
            price=price,
            volume_24h=volume_24h,
            volume_change_24h=volume_change_24h,
            percent_change_1h=percent_change_1h,
            percent_change_24h=percent_change_24h,
            percent_change_7d=percent_change_7d,
            percent_change_30d=percent_change_30d,
            market_cap=market_cap,
            market_cap_dominance=market_cap_dominance,
            fully_diluted_market_cap=fully_diluted_market_cap,
            tagString=tagString,
            num_market_pairs=num_market_pairs,
        )


@tool
def get_coin_tool(symbol: str):
    """
    When user wants to know price of crypto currency
    Args:
    symbol: Symbol of coin or token user need select it. Example : BTC, ETH, USDT
    """
    return ""
