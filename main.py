from flask import Flask
import pandas as pd
from faker import Faker
import mysql.connector
import csv

app = Flask(__name__)


@app.route('/')
def index():
    fake = Faker()
    data = {
        'id': [i + 1 for i in range(1000000)],  # Tạo 1 triệu id từ 1 đến 1000000
        'first_name': [fake.first_name() for _ in range(1000000)],
        'last_name': [fake.last_name() for _ in range(1000000)],
        'address': [fake.address() for _ in range(1000000)],
        'birthday': [fake.date_of_birth(minimum_age=18, maximum_age=90).strftime('%b-%d-%Y') for _ in range(1000000)]
    }

    df = pd.DataFrame(data)

    df.to_csv('user_data.csv', index=False)

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",
        database="test2"
    )
    mycursor = mydb.cursor()

    mycursor.execute("CREATE TABLE IF NOT EXISTS user ("
                     "id INT PRIMARY KEY,"
                     " first_name VARCHAR(255),"
                     " last_name VARCHAR(255),"
                     " address TEXT,"
                     " birthday VARCHAR(255))")

    with open('user_data.csv', 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Bỏ qua header
        for line in csv_reader:
            if len(line) == 5:
                id, first_name, last_name, address, birthday = line
                mycursor.execute(
                    "INSERT INTO user (id, first_name, last_name, address, birthday) VALUES (%s, %s, %s, %s, %s)",
                    (id, first_name, last_name, address, birthday))
            else:
                print("Dòng không hợp lệ:", line)

    mydb.commit()
    mydb.close()

    return "Data imported successfully!"
if __name__ == "__main__":
    app.run(debug=True)
