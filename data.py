import csv
import random
import time

# Output CSV filename
FILENAME = 'weather_data.csv'
NUM_ROWS = 50  # You can increase this to generate more data

cities = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad', 'Pune', 'Ahmedabad']
weathers = ['clear sky', 'partly cloudy', 'cloudy', 'rainy', 'thunderstorm', 'sunny', 'mist']

with open(FILENAME, mode='w', newline='') as file:
    writer = csv.writer(file)
    # Write CSV header
    writer.writerow(['city', 'temperature', 'humidity', 'weather', 'wind_speed', 'timestamp'])

    for _ in range(NUM_ROWS):
        city = random.choice(cities)
        temperature = round(random.uniform(20, 40), 2)  # in Celsius
        humidity = random.randint(30, 90)               # in %
        weather = random.choice(weathers)
        wind_speed = round(random.uniform(1, 10), 2)    # in m/s
        timestamp = int(time.time())                    # current UNIX time

        writer.writerow([city, temperature, humidity, weather, wind_speed, timestamp])

print(f"✅ Generated {NUM_ROWS} rows in {FILENAME}!")
