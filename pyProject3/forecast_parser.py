from typing import Dict, Any, List


def parse_daily_forecast(forecast_data: Dict[str, Any]) -> Dict[str, List[float] | List[str]]:
    daily_data = forecast_data.get("DailyForecasts", [])
    result: Dict[str, List[float] | List[str]] = {
        "dates": [],
        "min_temps": [],
        "max_temps": [],
        "wind_speeds": [],
        "precipitation_prob": []
    }

    for day_forecast in daily_data:
        date_str: str = day_forecast.get("Date", "").split("T")[0]

        temp = day_forecast.get("Temperature", {})
        temp_min = temp.get("Minimum", {}).get("Value", 0.0)
        temp_max = temp.get("Maximum", {}).get("Value", 0.0)

        day_part = day_forecast.get("Day", {})
        wind_info = day_part.get("Wind", {})
        wind_speed = wind_info.get("Speed", {}).get("Value", 0.0)

        precip_prob = day_part.get("PrecipitationProbability", 0.0)

        result["dates"].append(date_str)
        result["min_temps"].append(temp_min)
        result["max_temps"].append(temp_max)
        result["wind_speeds"].append(wind_speed)
        result["precipitation_prob"].append(precip_prob)

    return result
