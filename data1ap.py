from faker import Faker
import random
import csv
import time

fake = Faker()

with open('student_data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['name', 'grade', 'subject', 'marks', 'status', 'timestamp'])

    for _ in range(100):
        marks = random.randint(0, 100)
        writer.writerow([
            fake.first_name(),
            random.choice(['A', 'B', 'C', 'D', 'F']),
            random.choice(['Math', 'English', 'Science']),
            marks,
            'pass' if marks >= 40 else 'fail',
            int(time.time())
        ])
