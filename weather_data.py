import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry

cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

url = "https://archive-api.open-meteo.com/v1/archive"  

params = {
    "latitude": 12.9719,  # For now, we are extracting the data for the city of Bangalore, India
    "longitude": 77.5937,
    "start_date": "2023-03-01", 
    "end_date": "2024-03-30", 
    "hourly": [
        "temperature_2m",
        "relative_humidity_2m",
        "precipitation",
        "wind_speed_10m",
        "cloud_cover",
        "weather_code",
        "pressure_msl",
        "sunshine_duration"
    ],
    "timezone": "Asia/Kolkata"
}

responses = openmeteo.weather_api(url, params=params)
response = responses[0]

hourly = response.Hourly()
hourly_data = {
    "timestamp": pd.date_range(
        start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
        end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
        freq=pd.Timedelta(seconds=hourly.Interval()),
        inclusive="left"
    ),
    "temperature_2m": hourly.Variables(0).ValuesAsNumpy(),
    "humidity_2m": hourly.Variables(1).ValuesAsNumpy(),
    "precipitation": hourly.Variables(2).ValuesAsNumpy(),
    "wind_speed_10m": hourly.Variables(3).ValuesAsNumpy(),
    "cloud_cover": hourly.Variables(4).ValuesAsNumpy(),
    "weather_code": hourly.Variables(5).ValuesAsNumpy(),
    "pressure_msl": hourly.Variables(6).ValuesAsNumpy(),
    "sunshine_duration": hourly.Variables(7).ValuesAsNumpy()
}

weather_df = pd.DataFrame(data=hourly_data)

print(f"Total rows fetched: {len(weather_df)}")

weather_df.to_csv("weather_data_large.csv", index=False)
print("Weather data saved as weather_data_large.csv")
