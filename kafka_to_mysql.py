import csv
import mysql.connector
from mysql.connector import Error

try:
    connection = mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="root",
        database="customer_db"
    )

    if connection.is_connected():
        print("✅ Connected to MySQL!")

        cursor = connection.cursor()

        with open('weather_data.csv', mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                cursor.execute("""
                    INSERT INTO weather_db (city, temperature, humidity, weather, wind_speed, timestamp)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    row['city'],
                    float(row['temperature']),
                    int(row['humidity']),
                    row['weather'],
                    float(row['wind_speed']),
                    int(row['timestamp'])
                ))

        connection.commit()
        print("✅ Data inserted into MySQL!")

except Error as e:
    print(f"❌ Error: {e}")

finally:
    if 'cursor' in locals() and cursor:
        cursor.close()
    if 'connection' in locals() and connection.is_connected():
        connection.close()
        print("🔒 MySQL connection closed.")
