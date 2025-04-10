import requests

API_KEY = "13605077da5a71ae6987056ecfc6c9df"
CITY = "Delhi"
URL = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

response = requests.get(URL)
data = response.json()

print(data)
