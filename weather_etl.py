import requests
import csv
import os
# ==== CONFIG ====
API_KEY = "13605077da5a71ae6987056ecfc6c9df"
CITY = "Delhi"
URL = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
# ==== EXTRACT ====
response = requests.get(URL)
data = response.json()
# ==== TRANSFORM ====
transformed_data = {
    "city": data["name"],
    "temperature": data["main"]["temp"],
    "humidity": data["main"]["humidity"],
    "weather": data["weather"][0]["description"],
    "wind_speed": data["wind"]["speed"],
    "timestamp": data["dt"]
}
print("Transformed Weather Data:")
print(transformed_data)
# ==== LOAD ====
file_exists = os.path.isfile('weather_data.csv')
with open('weather_data.csv', mode='a', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=transformed_data.keys())
    
    if not file_exists:
        writer.writeheader()
    
    writer.writerow(transformed_data)

print("✅ Weather data saved to weather_data.csv")
