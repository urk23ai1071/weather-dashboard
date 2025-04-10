# kafka_to_mysql_student_consumer.py
from kafka import KafkaConsumer
import json
import mysql.connector

consumer = KafkaConsumer(
    'student_performance_topic',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

# MySQL connection
conn = mysql.connector.connect(
    host='localhost',
    user='youruser',
    password='yourpass',
    database='yourdb'
)
cursor = conn.cursor()

create_table_query = """
CREATE TABLE IF NOT EXISTS student_data (
    name VARCHAR(100),
    grade VARCHAR(10),
    subject VARCHAR(50),
    marks INT,
    status VARCHAR(10),
    timestamp BIGINT
);
"""
cursor.execute(create_table_query)

for message in consumer:
    data = message.value
    cursor.execute("""
        INSERT INTO student_data (name, grade, subject, marks, status, timestamp)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (data['name'], data['grade'], data['subject'], int(data['marks']), data['status'], int(data['timestamp'])))
    conn.commit()
    print("Inserted:", data)
