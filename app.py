from flask import Flask, render_template, jsonify, request, url_for, send_file
import mysql.connector
import json
import mysql.connector.pooling
import string
import random
import datetime
from datetime import timedelta
#pip install Flask-APScheduler
from apscheduler.schedulers.background import BackgroundScheduler
import smtplib
from email.mime.text import MIMEText
from openpyxl import Workbook
from dateutil.parser import parse
from collections import defaultdict

app = Flask(__name__)

#Scheduler initialisieren
scheduler = BackgroundScheduler()

#globaler Counter für Warnstufe des Bereichs, globale aktuelle Zeit
area_limits_global = {}
daily_warning_counter = {}
current_date = datetime.datetime.now().hour


domainname = "http://127.0.0.1:5000" 

# MySQL connection configuration
mysql_config = {    #change this to your own database
    'user': '',
    'password': '',
    'host': '',
    'database': '',
    'raise_on_warnings': True
}
# Pool of MySQL Connections, to handle multiple requests
pool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name="mypool", 
    pool_size=10, 
    pool_reset_session=True,# Adjust the maximum number of idle connections# Adjust the maximum connection lifetime in seconds
    **mysql_config)

#Funktion zur Mail Versendung
def send_email_warning(letter): #adjust this variables to your email address and recipients
    
    #Unsere Testmail
    recipient_email = ""
    
    sender_email = "" 
    username = ""
    password = ""   
    smtp_server = ""
    smtp_port = 1 #this aswell
    

    #Nachricht erstellen
    subject = f"Bereich {letter}: Lautstärke-Warnung"
    body = "Aufgrund des erhöhten Lärmpegels wird darauf hingewiesen, dass Maßnahmen zur Lärmreduzierung erforderlich sind!"
    
    #E-Mail erstellen
    message = MIMEText(body)
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = recipient_email
    
    #E-Mail versenden
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(username, password)
            server.sendmail(sender_email, recipient_email, message.as_string())
        print("E-Mail-Benachrichtigung gesendet!")
    except Exception as e:
        print("Fehler beim Senden der E-Mail-Benachrichtigung:", str(e))


#Berechnung Warnstufe der Bereiche
def schedulerWarnung():
    #Verbindung zu MySQL server aufbauen und Query ausführen
    con_warnung = pool.get_connection()
    cur_warnung = con_warnung.cursor()
    
    try:
        query_warnung = 'SELECT m.value, s.area FROM measurement m JOIN soundmeter s ON m.soundmeter_id = s.id WHERE m.soundmeter_id <= 19 AND m.time BETWEEN NOW() - INTERVAL 60 SECOND AND NOW();'
        cur_warnung.execute(query_warnung)
        result_warnung = cur_warnung.fetchall()
        
        #Average der Werte für jeden Bereich berechnen
        sums = {}
        counts = {}
        
        for value, letter in result_warnung:
            if letter in sums:
                sums[letter] += value
                counts[letter] += 1
            else:
                sums[letter] = value
                counts[letter] = 1
    
        averages = {letter: sums[letter] / counts[letter] for letter in sums}
        
        
        #Query für Lautstärkelimit aller Bereiche ausführen
        query_area_limit = 'SELECT DISTINCT area, soundlimit FROM soundmeter WHERE area NOT IN (%s, %s);'
        cur_warnung.execute(query_area_limit, ('1NA', '2NA', ))
        result_area_limit = cur_warnung.fetchall()
    
        reset_warning_counter()
    
        #Limit vergleichen mit berechnetem Average und dementsprechend globalen Counter hoch-/runterzählen
        for letter, average in averages.items():
            limit = next((limit for l, limit in result_area_limit if l == letter), None)
            if limit is not None:
                if average > limit:
                    if letter in area_limits_global:
                        area_limits_global[letter] += 1
                    else:
                        area_limits_global[letter] = 1
    
                    #falls in einem Bereich bereits 2 Warnungen gesendet wurden werden restlich ignoriert
                    if letter in daily_warning_counter and daily_warning_counter[letter] > 2:
                        print(f'Warnungslimit für Bereich {letter} erreicht')
                        if area_limits_global[letter] == 4:
                            area_limits_global[letter] = 0
                        continue
                   
                    if area_limits_global[letter] == 4:
                        print(f"Warnung: Der Bereich für den Buchstaben {letter} hat den Wert 4 erreicht!")
                        querynotification = "INSERT INTO notification (time, area) VALUES (NOW(), %s)"
                        cur_notification = con_warnung.cursor()
                        cur_notification.execute(querynotification, (letter, ))
                        con_warnung.commit()
                        send_email_warning(letter)
                        cur_notification.close()
                        
                        if letter in daily_warning_counter:
                            daily_warning_counter[letter] += 1
                        else:
                            daily_warning_counter[letter] = 1
                        
                        area_limits_global[letter] = 0
                else:
                    if letter in area_limits_global and area_limits_global[letter] > 0:
                        area_limits_global[letter] -= 1
                    elif letter not in area_limits_global:
                        area_limits_global[letter] = 0
    
        print("Bereichslevel:", area_limits_global)
    except Exception as e:
        print("This is the error: ", e)
    finally:
        cur_warnung.close()
        con_warnung.close()

    

def reset_warning_counter():
    global current_date
    global daily_warning_counter

    if datetime.datetime.now().hour > current_date:
        daily_warning_counter = {}
        current_date= datetime.datetime.now().hour


#Scheduler Job und Trigger zuweisen
scheduler.add_job(id='Scheduled Task', func= schedulerWarnung, max_instances= 3, trigger = 'interval', seconds = 60)


@app.route('/')
def index():
    return render_template('Deutsch/uebersicht.html')


@app.route('/overview')
def overview():
    return render_template('Englisch/overview.html')


@app.route('/heute')
def heute():
    return render_template('Deutsch/heute.html')


@app.route('/today')
def today():
    return render_template('Englisch/today.html')


@app.route('/woche')
def woche():
    return render_template('Deutsch/kalenderwoche.html')


@app.route('/week')
def week():
    return render_template('Englisch/week.html')


@app.route('/monat')
def monat():
    return render_template('Deutsch/monat.html')


@app.route('/month')
def month():
    return render_template('Englisch/month.html')


@app.route('/download')
def download_german():
    return render_template('Deutsch/download.html')


@app.route('/download_english')
def download_english():
    return render_template('Englisch/download.html')


@app.route('/administration')
def admin_german():
    return render_template('Deutsch/admin.html')


@app.route('/admin')
def admin_english():
    return render_template('Englisch/settings.html')


@app.route('/get_week_chart_data', methods=['POST']) # Responds with the content of the weekly chart
def get_week_chart_data():
    selected_option = request.json['selected_option1'] #week
    selected_option2 = request.json['selected_option2']  #area

    match selected_option2:
        case "area-a":
            selected_option2 ="A"
        case "area-b":
            selected_option2 ="B"
        case "area-c":
            selected_option2 ="C"
        case "area-d":
            selected_option2 ="D"
        case "area-e":
            selected_option2 ="E"
        case "area-f":
            selected_option2 ="F"
        case "area-g":
            selected_option2 ="G"
        case "area-h":
            selected_option2 ="H"
    date_monday,date_tuesday, date_wednesday, date_thursday, date_friday,date_saturday, week = format_week_dates(selected_option)

    connection = pool.get_connection()
    cursor = connection.cursor()

    try:

        query ="SELECT time, value FROM measurement m JOIN soundmeter s ON m.soundmeter_id = s.id WHERE s.area = %s AND time BETWEEN %s AND %s;"
        if(not selected_option2 or not date_monday or not date_friday):
            return(0,0,0)
        else:
            cursor = connection.cursor(dictionary=True)

            cursor.execute(query,(selected_option2, date_monday, date_saturday, )) #Monday 0:0:0 to Saturday 0:0:0 to get all weekdays

            # Create dictionaries to store values and times for each day
            days = {
                "Monday": {"times": [], "values": []},
                "Tuesday": {"times": [], "values": []},
                "Wednesday": {"times": [], "values": []},
                "Thursday": {"times": [], "values": []},
                "Friday": {"times": [], "values": []},
                "Saturday": {"times": [], "values": []},
                "Sunday": {"times": [], "values": []}
            }

            # Process the query results
            for row in cursor.fetchall():
                datetime_value = row['time']
                date = datetime_value.date()
                day_name = date.strftime("%A")

                # Append the time and value to the corresponding day's arrays
                days[day_name]["times"].append(datetime_value.time())
                days[day_name]["values"].append(row['value'])

        # monday_data={
        #     "labels": days["Monday"]["times"],
        #     "values": days["Monday"]["values"]
        # }

        # tuesday_data={
        #     "labels": days["Tuesday"]["times"],
        #     "values": days["Tuesday"]["values"]
        # }

        # wednesday_data={
        #     "labels": days["Wednesday"]["times"],
        #     "values": days["Wednesday"]["values"]
        # }

        # thursday_data={
        #     "labels": days["Thursday"]["times"],
        #     "values": days["Thursday"]["values"]
        # }

        # friday_data={
        #     "labels": days["Friday"]["times"],
        #     "values": days["Friday"]["values"]
        # }

        formatted_days = {}

        # Iterate over each day
        for day, data in days.items():
            times = data["times"]
            values = data["values"]
            
            # Convert times to the desired format
            formatted_times = [datetime.datetime.strptime(str(time), "%H:%M:%S").strftime("%H:00") for time in times]

            # Create a new dictionary entry with formatted times and values
            formatted_days[day] = {"times": formatted_times, "values": values}

            averaged_data = {}

            # Iterate over each day
            for day, data in formatted_days.items():
                times = data["times"]
                values = data["values"]
                
                # Initialize variables to calculate average
                average_sum = 0
                count = 0
                hourly_averages = {}  # Dictionary to store hourly averages for the specific day
                
                # Iterate over each label and value
                for time, value in zip(times, values):
                    # Check if the label is in the format "hh:xx"
                    if time[-5:-3].isdigit() and time[-2:] == "00":
                        hour = time[-5:-3]
                        average_sum += value
                        count += 1
                        hourly_averages[hour] = round(average_sum / count)

                # Add 0 values for hours with no data between 8:00 and 17:00
                for hour in range(8, 18):
                    hour_str = str(hour).zfill(2)
                    if hour_str not in hourly_averages:
                        hourly_averages[hour_str] = 0    
                
                # Store the hourly averages for the specific day
                averaged_data[day] = hourly_averages

            desired_labels = [str(hour).zfill(2) for hour in range(8, 18)]

            # Filter out labels not within the desired range for each day
            filtered_data = {}
            for day, labels in averaged_data.items():
                filtered_labels = {label: value for label, value in labels.items() if label in desired_labels}
                filtered_data[day] = filtered_labels

    except Exception as e:
        print("This is the error: ", e)

    finally:
        connection.close()
        cursor.close()

    chart_data = json.dumps(filtered_data, default=str)
    chart_data = eval(chart_data)
    return jsonify(chart_data, date_monday, date_friday, week)


@app.route('/get_chart_data', methods=['POST']) # Responds with content of either todays or monthly content
def get_chart_data():

    if(request.referrer == f"{domainname}/monat"
       or request.referrer == f"{domainname}/month"):

        selected_option = request.json['selected_option2']
        selected_month = request.json['selected_option1'].split("-")[1]
        selected_year = request.json['selected_option1'].split("-")[0]
    
    if(f"{domainname}/heute" in request.referrer 
       or f"{domainname}/today" in request.referrer):
        
        selected_option = request.json['selected_option1']

        match selected_option:
            case "area-a":
                selected_option ="A"
            case "area-b":
                    selected_option ="B"
            case "area-c":
                    selected_option ="C"
            case "area-d":
                    selected_option ="D"
            case "area-e":
                    selected_option ="E"
            case "area-f":
                    selected_option ="F"
            case "area-g":
                    selected_option ="G"
            case "area-h":
                    selected_option ="H"

    
    # Establish a connection to MySQL
    connection = pool.get_connection()
    cursor = connection.cursor()
    
    try:
        query=0
        if(request.referrer == f"{domainname}/monat" 
           or request.referrer == f"{domainname}/month"):
            query = "SELECT time, value FROM measurement m JOIN soundmeter s ON m.soundmeter_id = s.id WHERE s.area = %s AND MONTH(m.time) = %s AND YEAR(m.time) = %s;"
            if(not selected_option or not selected_month):
                return (0,0)
            else:
                cursor.execute(query, (selected_option,selected_month,selected_year))
        elif(f"{domainname}/heute" in request.referrer 
             or f"{domainname}/today" in request.referrer):
            query = "SELECT time, value FROM measurement m JOIN soundmeter s ON m.soundmeter_id = s.id WHERE s.area = %s AND DATE(m.time) = CURDATE();"
            if(not selected_option):
                return (0,0)
            else:     
                cursor.execute(query, (selected_option,))
        
        # Retrieve the data
        queryoutput = cursor.fetchall()
        chart_data = json.dumps(queryoutput, default=str)
        data = eval(chart_data)

        # Process the retrieved data as needed
        chart_data = []
        chart_labels = []
        
        for row in data:
            # Assuming the chart data is in a specific column of the retrieved data
            if(request.referrer == f"{domainname}/monat" 
               or request.referrer == f"{domainname}/month"):
                chart_labels.append(row[0].split()[0].split("-")[2])
            elif(f"{domainname}/heute" in request.referrer 
                 or f"{domainname}/today" in request.referrer):
                chart_labels.append(row[0].split()[1].split(":")[0])
                
            chart_data.append(row[1])

    except Exception as e:
        print("This is the error: ", e)

    finally:
        # Close the MySQL connection
        cursor.close()
        connection.close()

    unique_labels, averaged_data  = calculate_average(chart_data, chart_labels)

    if(f"{domainname}/heute" in request.referrer 
       or f"{domainname}/today" in request.referrer):

        for i in range(len(unique_labels)):
            # Add ":00" to each entry
            unique_labels[i] += ":00"

    if (averaged_data == []):
        return jsonify(averaged_data,unique_labels,)
    
    return jsonify(averaged_data,unique_labels, min(averaged_data), max(averaged_data),)


def calculate_average(values, labels):
    if len(values) != len(labels):
        return None, None
    
    if len(values) == 0 or len(labels) == 0:
        return None, None
    
    label_dict = {}
    
    # Map labels to corresponding values
    for value, label in zip(values, labels):
        if label in label_dict:
            label_dict[label].append(value)
        else:
            label_dict[label] = [value]
    
    unique_labels = []
    averages = []
    
    # Calculate average for each label
    for label, value_list in label_dict.items():
        unique_labels.append(label)
        averages.append(sum(value_list) / len(value_list))
    
    return unique_labels, averages


def get_latest_data():

    connection = pool.get_connection()
    cursor = connection.cursor()    
    
    
    try:
        query = """
            SELECT s.area AS Area, AVG(m.value) AS value
            FROM measurement m
            JOIN soundmeter s ON m.soundmeter_id = s.id
                WHERE s.area IN ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H')
                AND m.time IN (
                    SELECT MAX(time)
                    FROM measurement
                    WHERE soundmeter_id IN (SELECT id FROM soundmeter WHERE area IN ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'))
                    GROUP BY soundmeter_id
    )
    GROUP BY s.area
        """
    
        cursor.execute(query)
        results = cursor.fetchall()

        data = [row[1] for row in results]

    except Exception as e:
        print("This is the error: ", e)

    finally:
        cursor.close()
        connection.close()
    
    return data


@app.route('/refresh_overview', methods=['POST', 'GET'])
def refresh_overview():
    return jsonify(get_latest_data())


@app.route("/download_excel", methods=["POST"])
def download_excel():

    data = request.json  # Retrieve the JSON data from the request
    ids = data.get("ids")
    datetime1 = data.get("datetime1")
    datetime2 = data.get("datetime2")

    connection = pool.get_connection()
    cursor = connection.cursor()
    
    try:
        areas = [element.split("-")[1].upper() for element in ids]
        placeholders = ', '.join(['%s'] * len(areas))
    
        query = f"""
            SELECT s.area, m.value, m.time
                FROM measurement m
                JOIN soundmeter s ON m.soundmeter_id = s.id 
                WHERE s.area IN ({placeholders})
                AND m.time BETWEEN %s AND %s
        """
        values = areas + [datetime1, datetime2]  # Concatenate the values into a single list
        cursor.execute(query, values)
    
        # Fetch all the rows from the result set
        rows = cursor.fetchall()
        
    
        # Create a new Excel workbook and get the active worksheet
        workbook = Workbook()
        worksheet = workbook.active
    
        # Write the column headers
        column_headers = [column[0] for column in cursor.description]
        worksheet.append(column_headers)
    
        # Write the data rows
        for row in rows:
            worksheet.append(row)
    
        # Save the workbook
        file_path = "./downloaded_data.xls"
        workbook.save(file_path)

    except Exception as e:
        print("This is the error: ", e)

    finally:
        cursor.close()
        connection.close()
    
    return send_file(file_path, as_attachment=True)

def format_week_dates(week_value):
    # Splitting the week value into year and week parts
    year, week = map(int, week_value.split('-W'))

    # Calculating the first day (Monday) to the sixth day (Saturday)
    first_day = datetime.datetime.strptime(f"{year}-W{week}-1", "%Y-W%W-%w")
    second_day = first_day + timedelta(days=1)
    third_day = first_day + timedelta(days=2)
    fourth_day = first_day + timedelta(days=3)
    fifth_day = first_day + timedelta(days=4)
    sixth_day = first_day + timedelta(days=5)
    
    # Formatting the dates as YYYY-MM-DD
    first_day_formatted = first_day.strftime("%Y-%m-%d")
    second_day_formatted = second_day.strftime("%Y-%m-%d")
    third_day_formatted = third_day.strftime("%Y-%m-%d")
    fourth_day_formatted = fourth_day.strftime("%Y-%m-%d")
    fifth_day_formatted = fifth_day.strftime("%Y-%m-%d")
    sixth_day_formatted = sixth_day.strftime("%Y-%m-%d")
    
    return first_day_formatted, second_day_formatted, third_day_formatted, fourth_day_formatted, fifth_day_formatted,sixth_day_formatted, week


if __name__ == '__main__':
    scheduler.start()  #uncomment to activate the mail-warnings
    app.run(debug=True, use_reloader=False)
