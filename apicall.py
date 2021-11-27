import requests
from datetime import datetime
from datetime import timedelta
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def decide_to_water(days_info, window_size=8, rain_prob=75):
    
    window_size = window_size if window_size < 48 else 48
    i = 0
    weather = []
    
    for info in days_info:
        if i == window_size:
            break
        else:
            weather.append(info[6])
            i += 1
    
    # Probability of rain
    rain = weather.count("Rain") / len(weather)
    rain *= 100
    
    if rain > rain_prob:
        return True
    
    return False

def handle_time(time):
    
    gtm_time = datetime.utcfromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S')
    
    given_time = datetime.strptime(gtm_time, "%Y-%m-%d %H:%M:%S")

    gtm__3 = 3
    
    final_time = given_time - timedelta(hours=gtm__3)

    final_time = final_time.strftime('%d/%m/%Y %H:%M:%S')
    
    return final_time

lat = "-34.577214787893645"
lon = "-58.45574860378882"
part = "alerts"
API_KEY = "fb1764a5729d871a7ac8d937ba8d2bb8"

url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&appid={API_KEY}" # &exclude={part}

res = requests.get(url)
res_json = res.json()

current_weather = res_json["current"]

handle_time(1634845247)

two_days = res_json["hourly"]

two_days_info = dict()

for i, hour in enumerate(two_days):
    
    temp = hour["temp"] - 273.15
    pressure = hour["pressure"]
    humidity = hour["humidity"]
    uvi = hour["uvi"]
    clouds = hour["clouds"] # % de nubes
    wind_speed = hour["wind_speed"]
    weather = hour["weather"][0]["main"]
    weather_desc = hour["weather"][0]["description"]
    
    two_days_info[i] = [temp, pressure, humidity, uvi, clouds, wind_speed, weather, weather_desc]

data = [t for t in two_days_info.values()]

df = pd.DataFrame(data, columns=["temperature", "pressure", "humidity", "uvi", "clouds", "wind_speed", "weather", "weather_desc"])

plt.plot(df["temperature"])
plt.ylabel("Temperature")
plt.show()

decide_to_water(two_days_info.values(), 30, 50)