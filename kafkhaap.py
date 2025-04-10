cursor.execute("""
    INSERT INTO weather_db (city, temperature, humidity, weather, wind_speed, timestamp)
    VALUES (%s, %s, %s, %s, %s, %s)
""", (data['city'], data['temperature'], ...))
