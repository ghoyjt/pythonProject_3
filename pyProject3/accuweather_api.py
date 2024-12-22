from typing import Dict, Any, List
import requests

from config import ACCUWEATHER_API_KEY


def fetch_location_info(city_name: str) -> Dict[str, Any]:
    url: str = "http://dataservice.accuweather.com/locations/v1/cities/search"
    params: Dict[str, str] = {
        "apikey": ACCUWEATHER_API_KEY,
        "q": city_name,
        "language": "en-us"
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data: List[Dict[str, Any]] = response.json()

    if not data:
        raise ValueError(f"Город не найден: {city_name}")

    obj = data[0]
    location_key: str = obj.get("Key", "")
    geo_position: Dict[str, Any] = obj.get("GeoPosition", {})
    lat: float = geo_position.get("Latitude", 0.0)
    lon: float = geo_position.get("Longitude", 0.0)

    return {
        "key": location_key,
        "lat": lat,
        "lon": lon,
        "name": city_name
    }


def fetch_forecast_for_days(location_key: str, days: int) -> Dict[str, Any]:
    if days not in [1, 3, 5]:
        raise ValueError("Допустимое количество дней: 1, 3 или 5.")

    url: str = f"http://dataservice.accuweather.com/forecasts/v1/daily/5day/{location_key}"
    params: Dict[str, str] = {
        "apikey": ACCUWEATHER_API_KEY,
        "language": "en-us",
        "metric": "true"
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data: Dict[str, Any] = response.json()

    if "DailyForecasts" in data:
        data["DailyForecasts"] = data["DailyForecasts"][:days]

    return data
