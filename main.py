from typing import Any
from weather_api import get_current_weather, extract_data, get_5days_forecast, extract_forecast_data
from file_manager import load_data, save_favourite,  get_favorites

USER_MENU = """
--- Weather Dashboard ---
1. Check City Weather
2. Show Favorities
3. Add to Favorites
4. Check 5-Day Forecast
5. Exit
"""

FILE_PATH = "./data/favourite.json"

if __name__ == "__main__":
    data_list = load_data(FILE_PATH)
    temp_city: dict[str, Any]  | None = None
    while True:
        print(USER_MENU)
        user_input = input("Choose action: ").strip()

        if user_input == "1":
            city_input = input("Enter city name: ").strip()

            if not city_input:
                print("City name cannot be empty.")
                continue

            raw_data = get_current_weather(city_input)

            if raw_data:
                formatted_data = extract_data(raw_data)
                temp_city = formatted_data

                # F-string allows multi-line if you use parentheses implicitly or explicitly
                print(
                    f"\n--- Weather in {formatted_data['city']}, {formatted_data['country']} ---"
                )
                print(f"Temp:      {formatted_data['temperature']}°C")
                print(f"Condition: {formatted_data['condition']}")
                print(f"Humidity:  {formatted_data['humidity']}%")
                print(f"Wind:      {formatted_data['wind_speed']} m/s")
            else:
                print("Could not fetch weather data. Please check the city name.")
        elif user_input == "2":
            print(get_favorites(data_list))
        elif user_input == "3":
            if not temp_city:
                print("No city searched yet! Please use Option 1 first.")
                continue
                
            already_exists = any(item['city'] == temp_city['city'] for item in data_list)

            if already_exists:
                print(f"{temp_city['city']} is already in your favorites.")
            else:
                data_list.append(temp_city)
                save_favourite(FILE_PATH, data_list)
                print(f"{temp_city['city']} has been added to favorites.")
        elif user_input == "4":
            city_input = input("Enter city for forecast: ").strip()
            if not city_input:
                print("City name cannot be empty.")
                continue
            
            print(f"Fetching forecast for {city_input}...")
            raw_forecast = get_5days_forecast(city_input)

            if raw_forecast:
                # 2. Clean the data
                clean_forecast = extract_forecast_data(raw_forecast)
                
                # 3. Display it nicely using a loop
                print(f"\n--- 5-Day Forecast for {city_input} ---")
                print(f"{'Date':<20} | {'Temp':<12} | {'Condition'}")
                print("-" * 50)
                
                for day in clean_forecast:
                    # Optional: Format the date string to look nicer
                    # The API gives "2023-10-25 12:00:00"
                    date_only = day['datetime'].split(" ")[0] 
                    
                    print(f"{date_only:<20} | {day['temperature']}°C    | {day['weather']}")
                print("-" * 50)
            else:
                print("Could not fetch forecast.")
        elif user_input == "5":
            print("See you again!")
            break
        else:
            print("Invalid selection. Please enter 1-4.")
