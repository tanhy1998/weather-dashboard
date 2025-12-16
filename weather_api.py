import requests
import json
from datetime import datetime
from typing import Any, Optional  # Optional is great for return types that might fail
from config import API_KEY, BASE_URL, FORECAST_URL


# 1. Accept city as an ARGUMENT
def get_current_weather(city: str) -> Optional[dict[str, Any]]:
    # Construct URL
    url = f"{BASE_URL}?q={city}&appid={API_KEY}&units=metric"

    try:
        # 2. Removed 'verify=False' (It's insecure; only use if strictly necessary)
        response = requests.get(url, verify=False)
        response.raise_for_status()  # This raises error for 404 (Not Found)

        data = response.json()
        return data

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return None  # Return None explicitly so main.py knows it failed
    except Exception as err:
        print(f"An error occurred: {err}")
        return None


def extract_data(data: dict[str, Any]) -> dict[str, Any]:
    weather_data: dict[str, Any] = {
        "city": data["name"],
        "country": data["sys"]["country"],
        "temperature": data["main"]["temp"],
        "condition": data["weather"][0]["main"],
        "humidity": data["main"]["humidity"],
        "wind_speed": data["wind"]["speed"],
    }

    return weather_data


def get_5days_forecast(city: str) -> Optional[dict[str, Any]]:
    url = f"{FORECAST_URL}?q={city}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(url, verify=False)
        response.raise_for_status()  # This raises error for 404 (Not Found)

        data = response.json()
        return data

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return None
    except Exception as err:
        print(f"An error occurred: {err}")
        return None


def extract_forecast_data(data: dict[str, Any]) -> list[dict[str, Any]]:
    if not data:
        return []

    forecast_data = []

    for obj in data["list"]:
        dt_str = obj["dt_txt"]
        time_part = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S").strftime("%H:%M:%S")
        if time_part == "12:00:00":
            row = {
                "datetime": dt_str,
                "temperature": f"{obj["main"]["temp"]:.2f}",
                "weather": obj["weather"][0]["description"],
            }
            forecast_data.append(row)

    return forecast_data


if __name__ == "__main__":
    # Test with an argument now
    test_data = get_5days_forecast("Kuala Lumpur")
    if test_data:
        print(extract_forecast_data(test_data))
