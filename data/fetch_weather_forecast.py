import requests
import pandas as pd
import os
from datetime import datetime

API_KEY = 'ca85b93c3a9a4f7a422c1a26ec3e77ae'
# List of major cities/coordinates in Bangladesh (can be expanded)
CITIES = [
    {'name': 'Dhaka', 'lat': 23.8103, 'lon': 90.4125},
    {'name': 'Chittagong', 'lat': 22.3569, 'lon': 91.7832},
    {'name': 'Khulna', 'lat': 22.8456, 'lon': 89.5403},
    {'name': 'Rajshahi', 'lat': 24.3636, 'lon': 88.6241},
    {'name': 'Sylhet', 'lat': 24.8949, 'lon': 91.8687},
    {'name': 'Barisal', 'lat': 22.7010, 'lon': 90.3535},
    {'name': 'Rangpur', 'lat': 25.7439, 'lon': 89.2752},
]

FORECAST_HOURS = 48


def fetch_weather_forecast(csv_path=None):
    url = 'https://api.openweathermap.org/data/2.5/forecast'
    all_rows = []
    for city in CITIES:
        params = {
            'lat': city['lat'],
            'lon': city['lon'],
            'appid': API_KEY,
            'units': 'metric'
        }
        try:
            resp = requests.get(url, params=params, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            for entry in data['list']:
                dt = datetime.utcfromtimestamp(entry['dt'])
                if (dt - datetime.utcnow()).total_seconds() > FORECAST_HOURS * 3600:
                    continue
                row = {
                    'city': city['name'],
                    'datetime': dt,
                    'temp': entry['main']['temp'],
                    'humidity': entry['main']['humidity'],
                    'pressure': entry['main']['pressure'],
                    'rain_3h': entry.get('rain', {}).get('3h', 0),
                    'weather': entry['weather'][0]['main'],
                    'weather_desc': entry['weather'][0]['description']
                }
                all_rows.append(row)
        except Exception as e:
            print(f"Error fetching forecast for {city['name']}: {e}")
    df = pd.DataFrame(all_rows)
    if csv_path is None:
        csv_path = os.path.join(os.path.dirname(__file__), 'weather_forecast.csv')
    df.to_csv(csv_path, index=False)
    print(f"Saved to {csv_path}")

if __name__ == "__main__":
    fetch_weather_forecast() 