from src.utils.enum import LLMEnum, LLMModelEnum, ProfileEnum


LLM = [LLMEnum.OPEN_AI.value, LLMEnum.ANTHROPIC.value]
# OPEN_AI_MODELS = [
#     LLMModelEnum.OPEN_AI_3_5_TURBO.value,
#     LLMModelEnum.OPEN_AI_4_OMNI_MINI.value,
#     LLMModelEnum.OPEN_AI_4_TURBO.value,
#     LLMModelEnum.OPEN_AI_4_OMNI.value,
#     LLMModelEnum.OPEN_AI_4.value,
# ]

OPEN_AI_MODELS = [
    LLMModelEnum.OPEN_AI_3_5_TURBO.value,
    LLMModelEnum.OPEN_AI_4_OMNI_MINI.value,
]

ANTHROPIC_MODELS = [
    LLMModelEnum.ANTHROPIC_3_OPUS.value,
    LLMModelEnum.ANTHROPIC_3_HAIKU.value,
    LLMModelEnum.ANTHROPIC_3_SONNET.value,
]

PROFILES = [
    ProfileEnum.CREATIVE.value,
    ProfileEnum.BALANCE.value,
    ProfileEnum.PRECISE.value,
]

WEATHER_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Weather Information</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }}
        h3 {{
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background-color: #f2f2f2;
            font-weight: bold;
        }}
        tr:hover {{
            background-color: #f5f5f5;
        }}
    </style>
</head>
<body>
    <h3>Weather Information for {city}, {country}</h3>
    <table>
        <tr>
            <th>Parameter</th>
            <th>Value</th>
        </tr>
        <tr>
            <td>Temperature</td>
            <td>{temp}°C</td>
        </tr>
        <tr>
            <td>Feels like</td>
            <td>{feels_like}°C</td>
        </tr>
        <tr>
            <td>Humidity</td>
            <td>{humidity}%</td>
        </tr>
        <tr>
            <td>Pressure</td>
            <td>{pressure} hPa</td>
        </tr>
        <tr>
            <td>Visibility</td>
            <td>{visibility} km</td>
        </tr>
        <tr>
            <td>Wind</td>
            <td>{wind_speed} m/s, direction {wind_direction}°</td>
        </tr>
        <tr>
            <td>Cloudiness</td>
            <td>{cloudiness}%</td>
        </tr>
        <tr>
            <td>Rainfall (last 1h)</td>
            <td>{rainfall} mm</td>
        </tr>
        <tr>
            <td>Weather</td>
            <td>{weather_description}</td>
        </tr>
        <tr>
            <td>Sunrise</td>
            <td>{sunrise}</td>
        </tr>
        <tr>
            <td>Sunset</td>
            <td>{sunset}</td>
        </tr>
    </table>
</body>
</html>
"""

COIN_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Crypto Information</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }}

       .crypto-info {{
            font-family: Arial, sans-serif;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            border: 1px solid #ddd;
            border-radius: 8px;
            background-color: #f9f9f9;
        }}

        .crypto-name {{
            font-size: 2rem;
            margin-bottom: 10px;
            color: #2a9d8f;
        }}

        .crypto-symbol {{
            font-size: 1.2rem;
            color: #555;
        }}

        .crypto-details, .supply-info, .market-info, .additional-info {{
            list-style: none;
            padding: 0;
            margin-bottom: 20px;
        }}

        .crypto-details li, .supply-info li, .market-info li, .additional-info li {{
            margin-bottom: 5px;
        }}

        .section-title {{
            font-size: 1.5rem;
            margin-top: 20px;
            margin-bottom: 10px;
            color: #e76f51;
        }}

        .tags {{
            font-style: italic;
            color: #555;
        }}

    </style>
</head>
<body>
<div class="crypto-info">
    <h1 class="crypto-name">{name} <span class="crypto-symbol">({symbol})</span></h1>
    <ul class="crypto-details">
        <li><strong>ID</strong>: {id}</li>
        <li><strong>Slug</strong>: {slug}</li>
        <li><strong>Is Active</strong>: {is_active}</li>
        <li><strong>Is Fiat</strong>: {is_fiat}</li>
        <li><strong>Date Added</strong>: {date_added}</li>
        <li><strong>Rank</strong>: {cmc_rank}</li>
        <li><strong>Last Updated</strong>: {last_updated}</li>
    </ul>
    <h2 class="section-title">Supply Information</h2>
    <ul class="supply-info">
        <li><strong>Circulating Supply</strong>: {circulating_supply}</li>
        <li><strong>Total Supply</strong>: {total_supply}</li>
        <li><strong>Max Supply</strong>: {max_supply}</li>
    </ul>
    <h2 class="section-title">Market Information</h2>
    <ul class="market-info">
        <li><strong>Price (USD)</strong>: ${price}</li>
        <li><strong>24h Volume</strong>: {volume_24h}</li>
        <li><strong>24h Volume Change</strong>: {volume_change_24h}%</li>
        <li><strong>1h Change</strong>: {percent_change_1h}%</li>
        <li><strong>24h Change</strong>: {percent_change_24h}%</li>
        <li><strong>7d Change</strong>: {percent_change_7d}%</li>
        <li><strong>30d Change</strong>: {percent_change_30d}%</li>
        <li><strong>Market Cap</strong>: {market_cap}</li>
        <li><strong>Market Cap Dominance</strong>: {market_cap_dominance}%</li>
        <li><strong>Fully Diluted Market Cap</strong>: {fully_diluted_market_cap}</li>
    </ul>
    <h2 class="section-title">Tags</h2>
    <p class="tags">{tagString}</p>
    <h2 class="section-title">Additional Information</h2>
    <ul class="additional-info">
        <li><strong>Number of Market Pairs</strong>: {num_market_pairs}</li>
    </ul>
</div>
</body>
</html>
"""
