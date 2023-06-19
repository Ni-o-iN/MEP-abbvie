import datetime
import random
import string
import mysql.connector

# Connect to the MySQL database
cnx = mysql.connector.connect(
    user='141.19.176.122',
    password='j3Remy.J0hn',
    host='141.19.143.13',
    database='calmvie'
)
cursor = cnx.cursor()

# Generate a random datetime within the current day
l=0
for i in range(20000):
    l = l +1
    # Get the current date
    today = datetime.date.today()

    # Generate a random time between 8:00 and 17:00
    start_time = datetime.datetime(today.year, today.month, today.day, 8)
    end_time = datetime.datetime(today.year, today.month, today.day, 17)
    time_diff = end_time - start_time
    random_time = start_time + datetime.timedelta(seconds=random.randint(0, int(time_diff.total_seconds())))

    # Generate a random value between 30 and 110
    random_value = random.randint(30, 70)

    # Generate a random letter from A to H
    random_number = random.randint(1, 9)

    # Execute the INSERT query
    query = "INSERT INTO measurement VALUES (%s, %s, %s);"
    data = (random_time,  random_number,random_value)
    cursor.execute(query, data)

    # Commit the changes and close the database connection
    cnx.commit()
    print(l)
cursor.close()
cnx.close()