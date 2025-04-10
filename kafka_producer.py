import json
import time
import random
from kafka import KafkaProducer

# Connect to Kafka
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Sample cities and weather conditions
cities = ['Delhi', 'Mumbai', 'Bangalore', 'Chennai']
weather_conditions = ['clear sky', 'cloudy', 'rainy', 'stormy']

print("🌦️ Sending weather data to Kafka...")

while True:
    weather_data = {
        'city': random.choice(cities),
        'temperature': round(random.uniform(20, 40), 2),
        'humidity': random.randint(30, 90),
        'weather': random.choice(weather_conditions),
        'wind_speed': round(random.uniform(0.5, 10), 2),
        'timestamp': int(time.time())
    }

    print(f"📤 Sending: {weather_data}")
    producer.send('weather-topic', weather_data)

    time.sleep(2)  # Send data every 2 seconds
