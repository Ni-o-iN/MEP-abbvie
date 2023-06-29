# This shouls only be used for testing data or something like that

import datetime
import random
import string
import mysql.connector
import time

# Connect to the MySQL database
cnx = mysql.connector.connect(
    user='141.19.176.122',
    password='j3Remy.J0hn',
    host='141.19.143.13',
    database='calmvie'
)
cursor = cnx.cursor()

# # Generate a random datetime within the current day
# l=0
# #for i in range(27, -1, -1):
# # for x in range(8,13,1):
# for l in range(1):
#     #for a in range(1,10,1):# hier noch eine Schleife für jeden Bereich also for von 1 - 8, oben dann auf 2 oder so setzen, dann ist es schneller
#     try:
#         # Get the current date
#         today = datetime.date.today()
            
#         # Generate a random time between 8:00 and 17:00
#         start_time = datetime.datetime(today.year, today.month, today.day+1, 8, 0)
#         end_time = datetime.datetime(today.year, today.month, today.day+1, 8, 40)
#         time_diff = end_time - start_time
#         random_time = start_time + datetime.timedelta(seconds=random.randint(0, int(time_diff.total_seconds())))

#         # Generate a random value between 30 and 110
#         random_value = random.randint(60, 90)

#         # Generate a random letter from A to H
#         #random_number = random.randint(1, 9)
#         #random_number = 1
#         #random_number = random.randint(1,9)
#         # Execute the INSERT query
#         query = "INSERT INTO measurement VALUES (%s, %s, %s);"
#         data = (random_time, 1,random_value)
#         cursor.execute(query, data)

#         # Commit the changes and close the database connection
#         cnx.commit()
#         print(l)
#         time.sleep(1)

#     except Exception:
#         print("error")

while(True):
    random_number = random.randint(45,60)
    random_number2 = random.randint(45,60)
    random_number3 = random.randint(45,60)
    random_number4 = random.randint(45,60)
    random_number5 = random.randint(45,60)
    random_number6 = random.randint(45,60)
    random_number7 = random.randint(45,60)
    random_number8 = random.randint(45,60)
    random_number9 = random.randint(45,60)
    sql = "INSERT INTO measurement (time, soundmeter_id, value) VALUES (NOW(), %s, %s)"
    val = [
        (1,random_number),#If u want to have multiple soundmeter attached to the raspberry, you can add more values here.                               
        (3,random_number2),
        (4, random_number3),
        (5, random_number4),
        (6, random_number5),
        (7, random_number6),
        (8, random_number7),
        (9, random_number8)
        ]
    cursor.executemany(sql, val)
    cnx.commit()
    print("a")
    time.sleep(3)

cursor.close()
cnx.close()