import json
import mysql.connector
from kafka import KafkaConsumer

# Connect to Kafka topic
consumer = KafkaConsumer(
    'weather-topic',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='weather-group'
)

# Connect to MySQL
connection = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="root",
    database="customer_db"   # NOTE: No extra spaces!
)

cursor = connection.cursor()

print("📥 Listening for weather data from Kafka...")

for message in consumer:
    data = message.value
    print(f"✅ Received: {data}")

    cursor.execute("""
        INSERT INTO weather_db (city, temperature, humidity, weather, wind_speed, timestamp)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        data['city'],
        float(data['temperature']),
        int(data['humidity']),
        data['weather'],
        float(data['wind_speed']),
        int(data['timestamp'])
    ))
    connection.commit()
